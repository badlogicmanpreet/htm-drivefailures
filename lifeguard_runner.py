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

_LOGGER = logging.getLogger(__name__)

_INPUT_FILE = 'harddrive-smart-data-pp-to-train.csv'
_INPUT_DATA_FILE = 'harddrive-smart-data.csv'

_OUTPUT_PATH = "anomaly_scores.csv"

_ANOMALY_THRESHOLD = 0.9


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


def createModelAndProcess():
    _LOGGER.info('processing good drives')
    goodModel = getModel('good')
    goodModel.enableInference({'predictedField': 'class'})
    data = pd.read_csv('harddrive-smart-data-good.csv')
    dictionary = data.transpose().to_dict().values()

    counter = 0
    for row in dictionary:
        result = goodModel.run(row)
        if counter % 100 == 0:
            print "Read %i lines..." % counter

    _LOGGER.info('processing bad drives')
    badModel = getModel('bad')
    badModel.enableInference({'predictedField': 'class'})
    data = pd.read_csv('harddrive-smart-data-bad.csv')
    dictionary = data.transpose().to_dict().values()

    counter = 0
    for row in dictionary:
        result = badModel.run(row)
        if counter % 100 == 0:
            print "Read %i lines..." % counter

    _LOGGER.info('done processing drives')


def runHarddriveAnomaly(plot):
    shifter = InferenceShifter()
    if plot:
        output = nupic_anomaly_output.NuPICPlotOutput('Harddrive Learning')
    else:
        output = nupic_anomaly_output.NuPICFileOutput('Harddrive Learning')


    _LOGGER.info('start with anomaly detection...')
    model = getModel('good')
    model.enableInference({'predictedField': 'class'})

    _LOGGER.info('read data file...')

    data = pd.read_csv('harddrive-smart-data-test.csv')
    dictionary = data.transpose().to_dict().values()

    for row in dictionary:
        csvWriter = csv.writer(open(_OUTPUT_PATH, "wa"))
        csvWriter.writerow(["class", "anomaly_score"])
        result = model.run(row)

        if plot:
           result = shifter.shift(result)

        prediction = result.inferences["multiStepBestPredictions"][1]
        anomalyScore = result.inferences['anomalyScore']

        output.write('', result.rawInput["class"], prediction, anomalyScore)

        csvWriter.writerow([row["class"], anomalyScore])
        if anomalyScore > _ANOMALY_THRESHOLD:
            _LOGGER.info("Anomaly detected at [%s]. Anomaly score: %f.", result.rawInput["class"], anomalyScore)


print "Anomaly scores have been written to", _OUTPUT_PATH

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # select feature vector
    dataCleanser(_INPUT_FILE)

    # split data
    dataSplit()

    # create models and process all data sequentially
    createModelAndProcess()

    # run harddrive anomaly
    runHarddriveAnomaly(plot=True)
