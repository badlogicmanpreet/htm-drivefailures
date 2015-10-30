# htm-drivefailures
![Hard drive failure prediction](https://upload.wikimedia.org/wikipedia/commons/b/b9/Hard_disk_failure.jpeg "Hard drive failures")

Hard drive failure prediction using SMART data set

Data is available from Center for Magnetic Recording Research (CMRR) University of California, San Diego

J. F. Murray, G. F. Hughes, K. Kreutz-Delgado
'Comparison of machine learning methods for predicting failures in hard drives'
Journal of Machine Learning Research, vol 6, 2005.

##### Dataset : 
data/hardrive.csv lists 63 smart features collected from 300+ hardrives. After feature analysis 25 features which are most relevant are selected based on ZScore.

#####Type of Data :
Each line in the data section contains the data from one SMART read (2 hour time frame), with the last column either 1 (for drives that eventually failed) or 0 (for drives that were good throughout testing).

Predictive column 'class' is changed to 'String' as nupic attributes type doesn't support 'bool'.

#####Swarming :
To select best model Swarming is done using harddrive-smart-data-pp-to-train.csv, swarm_description describes the params for swarming. swarm.py is run to created the model_params. For debug purpose swarm is run under small mode.

#####LifeGuard Runner :
lifeguard_runner.py is used to create and save model.

######Order of data used for training:

harddrive-smart-data-pp-to-train.csv (thrice)

harddrive-smart-data-pp-shuffle.csv  (twice)

calculated accuracy - poor


