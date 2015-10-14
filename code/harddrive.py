from pkg_resources import resource_filename
from nupic.data.file_record_stream import FileRecordStream
import pandas as ps

__author__ = 'manpreet.singh'

# global dataset path
datasetpath = ''


# get data set
def getdatasetpath():
    global datasetpath
    datasetpath = resource_filename("nupic.datafiles", "extra/harddrive/harddrive.csv")
    print(datasetpath)
    with open(datasetpath) as inputFile:
        print
        for _ in xrange(8):
            count = 0
            for word in inputFile.next().strip().split(','):
                count += 1
            #print inputFile.next().strip().split()
            print(count)

# get data and prepare
def getdata():
    print("datasetpath : ", datasetpath)
    # df = ps.read_csv('/Library/Python/2.7/site-packages/nupic/datafiles/extra/harddrive/harddrive.csv', header=0, index_col=0)
    # print(type(df))
    # print(df.dtypes)
    # print('number of columns : ', len(df))

    #df[2] = ps.Dataframe({[int, float, float, float, float, float, float, float, float, float, float, float, float,
    #                        float, float, float, float, float, float, float, float, float, float, float, float, float,
    #                        float, float, float, float, float, float, float, float, float, float, float, float, float,
    #                        float, float, float, float, float, float, float, float, float, float, float, float, float,
    #                        float, float, float, float, float, float, float, float, float, float, float, float, float,
    #                        float, float, float, float, float, bool]})
    # print(df.head(3))
    # print(df.tail(3))


    return FileRecordStream(datasetpath)


def printdata():
    data = getdata()
    print('fieldnames : ', data.getFieldNames())
    for _ in xrange(5):
        print data.next()


if __name__ == '__main__':
    getdatasetpath()
    printdata()
