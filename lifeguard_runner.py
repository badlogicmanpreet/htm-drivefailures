from __future__ import division
__author__ = 'manpreet.singh'

import sys
import importlib
import csv
import datetime
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager
import time
from collections import deque
import matplotlib.pyplot as plt
import csv
import pandas as pd

import nupic_output

DATA_CENTER_NAME = 'harddrive-smart-data-pp'
DATA_DIR = '.'
# '7/2/10 0:00'
DATE_FORMAT = "%m/%d/%y %H:%M"

# hack
SECONDS_PER_STEP = 0.5
WINDOW = 60
# turn matplotlib interactive mode on (ion)
plt.ion()
fig = plt.figure()
# plot title, legend, etc
plt.title('Harddrive prediction example')
plt.xlabel('time [s]')
plt.ylabel('failures')

DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)


_METRIC_SPECS = (
    MetricSpec(field='class', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
    MetricSpec(field='class', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'aae', 'window': 1000, 'steps': 1}),
    MetricSpec(field='class', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
    MetricSpec(field='class', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'altMAPE', 'window': 1000, 'steps': 1}),
)

def checkAccuracy() :
    print()

def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


def runIoThroughNupic(inputData, model, dataCenterName, plot):

    # hacking for trial
    data = pd.read_csv(inputData)
    dictionary = data.transpose().to_dict().values()

    # shifter = InferenceShifter()
    #
    # # hack
    # # Keep the last WINDOW predicted and actual values for plotting.
    # actHistory = deque([0.0] * WINDOW, maxlen=60)
    # predHistory = deque([0.0] * WINDOW, maxlen=60)
    #
    # # Initialize the plot lines that we will update with each new record.
    # actline, = plt.plot(range(WINDOW), actHistory)
    # predline, = plt.plot(range(WINDOW), predHistory)
    # # Set the y-axis range.
    # actline.axes.set_ylim(0, 2)
    # predline.axes.set_ylim(0, 2)

    counter = 0
    correct = 0;
    for row in dictionary:
        counter += 1

        actual = row['class']

        # actHistory.append(actual)

        result = model.run(row)

        if counter % 100 == 0:
            print "Read %i lines..." % counter

        # if plot:
        #     result = shifter.shift(result)

        prediction = result.inferences["multiStepBestPredictions"][1]

        # predHistory.append(prediction)

        # hack
        # write to a file
        rec = [[actual, prediction]]
        if actual == prediction:
            correct += 1
        #csv_writer(rec, 'result.csv')

        # hack
        # Redraw the chart with the new data.
        # actline.set_ydata(actHistory)  # update the data
        # predline.set_ydata(predHistory)  # update the data
        # plt.draw()
        # plt.legend(('actual', 'predicted'))

        # Make sure we wait a total of 2 seconds per iteration.
        # try:
        #     plt.pause(SECONDS_PER_STEP)
        # except:
        #     pass

    print('Number of %d correct predictions out of %d counter are %f' % (correct, counter, float(correct/counter) * 100))

def getModelParamsFromName(dataCenterName):
    importName = 'model_params.%s_model_params' % (dataCenterName.replace(' ', '_').replace('-', '_'))
    print 'import model params from %s' % importName
    try:
        importedModelParams = importlib.import_module(importName).MODEL_PARAMS
    except ImportError:
        raise Exception('No model params exist for %s' % dataCenterName)
    return importedModelParams


def createModel(modelParams):
    #model = ModelFactory.create(modelParams)
    #model.save('/Users/manpreet.singh/Sandbox/codehub/github/datascience/workspace/cortical/harddrive_lifeguard/model/model0')
    model = ModelFactory.loadFromCheckpoint('/Users/manpreet.singh/Sandbox/codehub/github/datascience/workspace/cortical/harddrive_lifeguard/model/model0')
    model.enableInference({'predictedField': 'class'})

    #model.disableLearning()

    # model = ModelFactory.create(modelParams)
    # model.enableInference({'predictedField': 'class'})
    return model


def runModel(dataCenterName, plot):
    model = createModel(getModelParamsFromName(dataCenterName))
    inputData = '%s/%s.csv' % (DATA_DIR, dataCenterName.replace(' ', '_'))
    print(inputData)
    inputData = './harddrive-smart-data-pp-shuffled.csv'
    runIoThroughNupic(inputData, model, dataCenterName, plot)

if __name__ == '__main__':
    print(DESCRIPTION)
    plot = False
    args = sys.argv[1:]
    if '--plot' in args:
        plot = True
        print('ploting')
    runModel(DATA_CENTER_NAME, plot=plot)

