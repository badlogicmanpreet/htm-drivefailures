__author__ = 'manpreet.singh'

import os
import pprint

#from swarm_description import SWARM_DESCRIPTION
from swarm_description import SWARM_DESCRIPTION
from nupic.swarming import permutations_runner

INPUT_FILE = 'harddrive-smart-data-pp-to-train.csv'

def modelParamsToString(modelParams):
    pp = pprint.PrettyPrinter(indent=2)
    return pp.pformat(modelParams)


def writeModelParamsToFile(modelParams, name):
    cleanName = name.replace(' ', '_').replace('-', '_')
    paramsName = '%s_model_params.py' % cleanName
    outDir = os.path.join(os.getcwd(), 'model_params')
    if not os.path.isdir(outDir):
        os.mkdir(outDir)
    outPath = os.path.join(os.getcwd(), 'model_params', paramsName)
    with open(outPath, 'wb') as outFile:
        modelParamsString = modelParamsToString(modelParams)
        outFile.write('MODEL_PARAMS = \\\n%s' % modelParamsString)
    return outPath


def swarmForBestModelParams(swarmConfig, name, maxWorkers = 9):
    outputLabel = name
    permWorkDir = os.path.abspath('swarm')
    if not os.path.exists(permWorkDir):
        os.mkdir(permWorkDir)
    modelParams = permutations_runner.runWithConfig(
        swarmConfig,
        {'maxWorkers': maxWorkers, 'overwrite': True},
        outputLabel=outputLabel,
        outDir=permWorkDir,
        permWorkDir=permWorkDir,
        verbosity=0
    )
    modelParamsFile = writeModelParamsToFile(modelParams, name)
    return modelParamsFile


def printSwarmSizeWarning(size):
    if size is 'small':
        print 'This is Debug Swarm, dont expect your model to produce great results'
    elif size is 'medium':
        print 'This will take some time, grab a cup of coffee'
    else:
        print 'Catchup some sleep :)'


def swarm(filePath):
    name = os.path.splitext(os.path.basename(filePath))[0]
    print '=================================='
    print 'swarming on %s data ... ' % name
    printSwarmSizeWarning(SWARM_DESCRIPTION['swarmSize'])
    print '=================================='
    modelParams = swarmForBestModelParams(SWARM_DESCRIPTION, name)
    print '\nWrote following model params file:'
    print '\t%s' % modelParams


if __name__ == '__main__':
    swarm(INPUT_FILE)
