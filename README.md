# htm-drivefailures
![Hard drive failure prediction](https://upload.wikimedia.org/wikipedia/commons/b/b9/Hard_disk_failure.jpeg "Hard drive failures")

Hard drive failure prediction using SMART data set

Data is available from Center for Magnetic Recording Research (CMRR) University of California, San Diego

J. F. Murray, G. F. Hughes, K. Kreutz-Delgado
'Comparison of machine learning methods for predicting failures in hard drives'
Journal of Machine Learning Research, vol 6, 2005.

##### Dataset : 
data/hardrive.csv lists 63 smart features collected from 300+ hardrives. After feature analysis 25 features which are most relevant are selected based on ZScore. With further analysis, 11 most effective features are retained for anomaly detection.

#####Type of Data :
Each line in the data section contains the data from one SMART read (2 hour time frame), with the last column either 1 (for drives that eventually failed) or 0 (for drives that were good throughout testing).

#####Swarming :
Not required

#####LifeGuard Runner :
lifeguard_runner.py is used to create and save model for both good and bad drives, it also runs the test data through models to get anomaly score.

######Training result:
In progress


