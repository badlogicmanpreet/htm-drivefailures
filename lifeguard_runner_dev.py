__author__ = 'manpreet.singh'

import pandas as pd
import logging
import csv
from nupic.frameworks.opf.modelfactory import ModelFactory
from model_params.harddrive_smart_data_model_params import MODEL_PARAMS
import numpy as np
import os
from nupic.data.inference_shifter import InferenceShifter
import nupic_anomaly_output
import datetime
import anomaly_plot as anplt
import time
from nupic.research.TP import TP

_LOGGER = logging.getLogger(__name__)

_INPUT_FILE = 'harddrive-smart-data-pp-to-train.csv'
_INPUT_DATA_FILE = 'harddrive-smart-data.csv'

_OUTPUT_PATH = "anomaly_scores.csv"

_ANOMALY_THRESHOLD = 0.9

# '7/2/10 0:00'
DATE_FORMAT = "%m/%d/%y %H:%M:%S"


# utility to convert to float
def convertorToFloat(val):
    if val == 'True':
        val = 1
    elif val == 'False':
        val = 0
    elif val is False:
        val = 0
    return val


# select feature set
def dataCleanser(inputFile):
    df = pd.read_csv(inputFile)

    colsToDrop = ['GList1', 'PList', 'Servo1', 'Servo2', 'Servo3', 'Servo5',
                  'ReadError1', 'ReadError2', 'ReadError3', 'FlyHeight5',
                  'ReadError18', 'ReadError19', 'Servo7', 'Servo8', 'ReadError20', 'GList2',
                  'GList3', 'Servo10']
    df = df.drop(colsToDrop, axis=1)

    df['class'] = df['class'].apply(convertorToFloat)

    df.to_csv('harddrive-smart-data-temp.csv', sep=',', index=False)

    df = pd.read_csv('harddrive-smart-data-temp.csv')
    df = df.convert_objects(convert_numeric=True)
    print(df.dtypes)
    df.to_csv('harddrive-smart-data.csv', sep=',', index=False)


def get_train_test_inds(y,train_proportion=0.7):
    '''Generates indices, making random stratified split into training set and testing sets
    with proportions train_proportion and (1-train_proportion) of initial sample.
    y is any iterable indicating classes of each observation in the sample.
    Initial proportions of classes inside training and
    testing sets are preserved (stratified sampling).
    '''

    y=np.array(y)
    y.setflags(write=True)
    train_inds = np.zeros(len(y),dtype=bool)
    test_inds = np.zeros(len(y),dtype=bool)
    values = np.unique(y)
    for value in values:
        value_inds = np.nonzero(y==value)[0]
        value_inds.setflags(write=True)
        np.random.shuffle(value_inds)
        n = int(train_proportion*len(value_inds))

        train_inds[value_inds[:n]]=True
        test_inds[value_inds[n:]]=True

    return train_inds,test_inds


# split data into good and bad drives, also training and test data
def dataSplit():
    df = pd.read_csv('harddrive-smart-data.csv')
    dfBad = df.loc[df['class'] == 1.0]
    dfGood = df.loc[df['class'] == 0.0]

    dfBad.to_csv('harddrive-smart-data-bad.csv', sep=',', index=False)
    dfGood.to_csv('harddrive-smart-data-good.csv', sep=',', index=False)

    print(dfBad.shape)
    print(dfGood.shape)

    # train_inds_bad, test_inds_bad = get_train_test_inds(dfBad)
    # train_inds_good, test_inds_good = get_train_test_inds(dfGood)
    #
    # dfBadTrain = dfBad[train_inds_bad]
    # dfBadTest = dfBad[test_inds_bad]
    #
    # dfGoodTrain = dfGood[train_inds_good]
    # dfGoodTest = dfGood[test_inds_good]
    #
    # dfBadTrain.to_csv('harddrive-smart-data-bad-train.csv', sep=',', index=False)
    # dfBadTest.to_csv('harddrive-smart-data-bad-test.csv', sep=',', index=False)
    #
    # dfGoodTrain.to_csv('harddrive-smart-data-good-train.csv', sep=',', index=False)
    # dfGoodTest.to_csv('harddrive-smart-data-good-test.csv', sep=',', index=False)

'''
Create singleton models with active learning
'''
def getModel(flag):

    modelDir = os.getcwd() + '/model/%s' % flag

    _LOGGER.info(modelDir)

    if os.path.exists(modelDir):
        _LOGGER.info('model exists')
        model = ModelFactory.loadFromCheckpoint(modelDir)
        return model
    else:
        _LOGGER.info('creating new model')
        model = ModelFactory.create(MODEL_PARAMS)
        model.save(modelDir)
        return model


'''
get saved models and process data sequentially. reset happens after 300 records/ drive
'''
def createModelAndProcess():
    _LOGGER.info('processing good drives')
    goodModel = getModel('good')
    goodModel.enableInference({'predictedField': 'class'})

    inputFile = open('harddrive-smart-data-good.csv', "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()

    counter = 0
    for row in csvReader:
        counter += 1

        FlyHeight6 = float(row[0])
        FlyHeight7 = float(row[1])
        FlyHeight8 = float(row[2])
        FlyHeight9 = float(row[3])
        FlyHeight10 = float(row[4])
        FlyHeight11 = float(row[5])
        FlyHeight12 = float(row[6])
        classV = float(row[7])

        result = goodModel.run({
            "FlyHeight6": FlyHeight6,
            "FlyHeight7": FlyHeight7,
            "FlyHeight8": FlyHeight6,
            "FlyHeight9": FlyHeight6,
            "FlyHeight10": FlyHeight6,
            "FlyHeight11": FlyHeight6,
            "FlyHeight12": FlyHeight6,
            "class": classV
            })
        if counter % 300 == 0:
            goodModel.resetSequenceStates()
            print "Read %i lines and reset done..." % counter

    inputFile.close()

    _LOGGER.info('processing bad drives')
    badModel = getModel('bad')
    badModel.enableInference({'predictedField': 'class'})
    inputFile = open('harddrive-smart-data-bad.csv', "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()

    counter = 0
    for row in csvReader:
        counter += 1

        FlyHeight6 = float(row[0])
        FlyHeight7 = float(row[1])
        FlyHeight8 = float(row[2])
        FlyHeight9 = float(row[3])
        FlyHeight10 = float(row[4])
        FlyHeight11 = float(row[5])
        FlyHeight12 = float(row[6])
        classV = float(row[7])

        result = badModel.run({
            "FlyHeight6": FlyHeight6,
            "FlyHeight7": FlyHeight7,
            "FlyHeight8": FlyHeight6,
            "FlyHeight9": FlyHeight6,
            "FlyHeight10": FlyHeight6,
            "FlyHeight11": FlyHeight6,
            "FlyHeight12": FlyHeight6,
            "class": classV
            })
        if counter % 300 == 0:
            badModel.resetSequenceStates()
            print "Read %i lines and reset done..." % counter

    inputFile.close()

    _LOGGER.info('done processing drives')

'''
run temporal anomaly to get the predictions and anomaly score, plot them.
Learning is disabled.
Results are saved to CSV for post analytics
nupic_output - used for plotting
'''
def runHarddriveAnomaly(plot):
    shifter = InferenceShifter()

    _LOGGER.info('start with anomaly detection...')

    model = getModel('good')
    model.enableInference({'predictedField': 'class'})
    # model.disableLearning()

    _LOGGER.info('read data file...')

    inputFile = open('harddrive-smart-data-good-test.csv', "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()


    csvWriter = csv.writer(open(_OUTPUT_PATH, "wa"))
    csvWriter.writerow(["class", "Prediction", "anomaly_score"])

    output = anplt.NuPICPlotOutput('HarddriveDetection')

    for row in csvReader:
        FlyHeight6 = float(row[0])
        FlyHeight7 = float(row[1])
        FlyHeight8 = float(row[2])
        FlyHeight9 = float(row[3])
        FlyHeight10 = float(row[4])
        FlyHeight11 = float(row[5])
        FlyHeight12 = float(row[6])
        classV = float(row[7])

        timestamp = datetime.datetime.strptime(datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT)

        result = model.run({
            "FlyHeight6": FlyHeight6,
            "FlyHeight7": FlyHeight7,
            "FlyHeight8": FlyHeight6,
            "FlyHeight9": FlyHeight6,
            "FlyHeight10": FlyHeight6,
            "FlyHeight11": FlyHeight6,
            "FlyHeight12": FlyHeight6,
            "class": classV
            })

        if plot:
           result = shifter.shift(result)

        prediction = result.inferences["multiStepBestPredictions"][1]
        anomalyScore = result.inferences['anomalyScore']

        # output.write(timestamp, result.rawInput["class"], prediction, anomalyScore)

        # csvWriter.writerow([row])
        # csvWriter.writerow('--------------------------------------------------')
        # csvWriter.writerow([result.rawInput['class'], prediction, anomalyScore])
        output.write(timestamp, result.rawInput['class'], prediction, anomalyScore)

        # _LOGGER.info('plotted')

        if anomalyScore > _ANOMALY_THRESHOLD:
            _LOGGER.info("Anomaly detected at [%s]. Anomaly score: %f.", result.rawInput["class"], anomalyScore)

        # time.sleep(1)


def findGoodOrBad():

    inputFile = open('harddrive-smart-data-goodbad-test.csv', "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()

    _LOGGER.info('evaluate models')
    goodModel = getModel('good')
    goodModel.enableInference({'predictedField': 'class'})

    badModel = getModel('bad')
    badModel.enableInference({'predictedField': 'class'})

    for row in csvReader:
        FlyHeight6 = float(row[0])
        FlyHeight7 = float(row[1])
        FlyHeight8 = float(row[2])
        FlyHeight9 = float(row[3])
        FlyHeight10 = float(row[4])
        FlyHeight11 = float(row[5])
        FlyHeight12 = float(row[6])
        classV = float(row[7])

        resultG = goodModel.run({
            "FlyHeight6": FlyHeight6,
            "FlyHeight7": FlyHeight7,
            "FlyHeight8": FlyHeight6,
            "FlyHeight9": FlyHeight6,
            "FlyHeight10": FlyHeight6,
            "FlyHeight11": FlyHeight6,
            "FlyHeight12": FlyHeight6,
            "class": classV
            })
        predictionG = resultG.inferences["multiStepBestPredictions"][1]
        anomalyScoreG = resultG.inferences['anomalyScore']
        print(predictionG, anomalyScoreG)

        resultB = badModel.run({
            "FlyHeight6": FlyHeight6,
            "FlyHeight7": FlyHeight7,
            "FlyHeight8": FlyHeight6,
            "FlyHeight9": FlyHeight6,
            "FlyHeight10": FlyHeight6,
            "FlyHeight11": FlyHeight6,
            "FlyHeight12": FlyHeight6,
            "class": classV
            })
        predictionB = resultB.inferences["multiStepBestPredictions"][1]
        anomalyScoreB = resultB.inferences['anomalyScore']
        print(predictionB, anomalyScoreB)

print "Anomaly scores have been written to", _OUTPUT_PATH

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    '''
    # select feature vector
    dataCleanser(_INPUT_FILE)

    # split data
    dataSplit()

    # create models and process all data sequentially
    createModelAndProcess()
    '''

    # find drive is good or bad
    findGoodOrBad()

    # run harddrive anomaly
    runHarddriveAnomaly(plot=True)

    _LOGGER.info('Finally done with Anomaly Detection')