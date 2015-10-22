from pkg_resources import resource_filename
from nupic.data.file_record_stream import FileRecordStream
from nupic.frameworks.opf.modelfactory import ModelFactory
from model_0 import model_params

from nupic.data.inference_shifter import InferenceShifter
from collections import deque
import time

import matplotlib.pyplot as plt

SECONDS_PER_STEP = 0.5
WINDOW = 60

# turn matplotlib interactive mode on (ion)
plt.ion()
fig = plt.figure()
# plot title, legend, etc
plt.title('Harddrive prediction example')
plt.xlabel('time [s]')
plt.ylabel('failures')

__author__ = 'manpreet.singh'

# global dataset path
datasetpath = ''


# get data set
def getdatasetpath():
    global datasetpath
    datasetpath = resource_filename("nupic.datafiles", "extra/harddrive/harddrive1.csv")
    print(datasetpath)
    with open(datasetpath) as inputFile:
        print
        for _ in xrange(8):
            count = 0
            for word in inputFile.next().strip().split(','):
                count += 1
            # print(count)


# get data and prepare
def getdata():
    print("datasetpath : ", datasetpath)
    return FileRecordStream(datasetpath)


def printdata():
    data = getdata()
    print('fieldnames : ', data.getFieldNames())
    for _ in xrange(5):
        print data.next()


def createmodel():
    #model = ModelFactory.create(model_params.MODEL_PARAMS)
    #model.save('/Users/manpreet.singh/Sandbox/codehub/github/htm-drivefailures/models/model0')
    model = ModelFactory.loadFromCheckpoint('/Users/manpreet.singh/Sandbox/codehub/github/htm-drivefailures/models/model0')
    model.enableInference({'predictedField': 'class'})

    # The shifter will align prediction and actual values.
    shifter = InferenceShifter()
    # Keep the last WINDOW predicted and actual values for plotting.
    actHistory = deque([0.0] * WINDOW, maxlen=60)
    predHistory = deque([0.0] * WINDOW, maxlen=60)

    # Initialize the plot lines that we will update with each new record.
    actline, = plt.plot(range(WINDOW), actHistory)
    predline, = plt.plot(range(WINDOW), predHistory)
    # Set the y-axis range.
    actline.axes.set_ylim(0, 2)
    predline.axes.set_ylim(0, 2)

    data = getdata()

    while True:
        s = time.time()

        print(data.next())

        record = dict(zip(data.getFieldNames(), data.next()))
        result = shifter.shift(model.run(record))
        # Update the trailing predicted and actual value deques.
        inference = result.inferences['multiStepBestPredictions'][1]
        if inference is not None:
            rawinput = result.rawInput['class']
            if rawinput == 'True':
                rawinput = 1
            else:
                rawinput = 0
            actHistory.append(rawinput)

            if inference == 'True':
                inference = 1
            else:
                inference = 0
            predHistory.append(inference)

            # Redraw the chart with the new data.
        actline.set_ydata(actHistory)  # update the data
        predline.set_ydata(predHistory)  # update the data
        plt.draw()
        plt.legend(('actual', 'predicted'))

        # Make sure we wait a total of 2 seconds per iteration.
        try:
            plt.pause(SECONDS_PER_STEP)
        except:
            pass

    #data = getdata()
    #for _ in xrange(100):
     #   record = dict(zip(data.getFieldNames(), data.next()))
     #   print "input: ", record["class"]
     #  result = model.run(record)
     #   print "prediction: ", result.inferences["multiStepBestPredictions"][1]


if __name__ == '__main__':
    getdatasetpath()
    printdata()
    createmodel()
