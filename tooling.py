__author__ = 'manpreet.singh'

import pandas as pd
import random

df = ''


def readcsv():
    global df
    df = pd.read_csv('harddrive-smart-data-pp-to-shuffle.csv')
    print(df.head())
    classv = df['class']


def convert(val):
    if val == '1':
        val = 'True'
    elif val == 0:
        val = 'False'
    # else:
    #     print('done')
    return val


def convertor(val):
    if val == '1':
        val = 'True'
    elif val == '0':
        val = 'False'
    elif val == 0:
        val = 'False'
    elif val == 1:
        val = 'TRUE'
    return val


def convertorToFloat(val):
    if val == 'True':
        val = 1
    elif val == 'False':
        val = '0'
    return val


def shuffle(df):
    index = list(df.index)
    random.shuffle(index)
    df = df.ix[index]
    df.reset_index()
    return df

if __name__ == '__main__':
    # readcsv()
    # print(df.shape)
    # df['class'] = df['class'].apply(convertorToFloat)
    # print(df['class'])
    # df.to_csv('harddrive1_pp.csv', sep=',', index=False)

    readcsv()
    print(df.shape)
    df = shuffle(df)
    df.to_csv('harddrive-smart-data-pp-shuffled.csv', sep=',', index=False)