__author__ = 'manpreet.singh'

import pandas as pd

df = pd.read_csv('harddrive.csv')
# print(df.head())

classv = df['class']


# print(classv)

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


df['class'] = df['class'].apply(convertor)

print(df['class'])

df.to_csv('harddrive1.csv', sep=',', index=False)