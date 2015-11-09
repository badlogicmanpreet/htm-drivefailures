__author__ = 'manpreet.singh'

import os
import shutil

def cleanup():

    path = os.getcwd()+'/model'

    # remove good and bad models
    if os.path.exists(path+'/good'):
        shutil.rmtree(path+'/good')

    if os.path.exists(path+'/bad'):
        shutil.rmtree(path+'/bad')

    if os.path.isfile(os.getcwd()+'/anomaly_scores.csv'):
        os.remove(os.getcwd()+'/anomaly_scores.csv')

    if os.path.isfile(os.getcwd()+'/harddrive-smart-data-temp.csv'):
        os.remove(os.getcwd()+'/harddrive-smart-data-temp.csv')

    if os.path.isfile(os.getcwd()+'/harddrive-smart-data.csv'):
        os.remove(os.getcwd()+'/harddrive-smart-data.csv')

    if os.path.isfile(os.getcwd()+'/harddrive-smart-data-good.csv'):
        os.remove(os.getcwd()+'/harddrive-smart-data-good.csv')

    if os.path.isfile(os.getcwd()+'/harddrive-smart-data-bad.csv'):
        os.remove(os.getcwd()+'/harddrive-smart-data-bad.csv')


if __name__ == '__main__':
    cleanup()
