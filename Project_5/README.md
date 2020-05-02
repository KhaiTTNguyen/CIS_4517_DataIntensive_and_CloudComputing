# Overview 
This folder consists of a Bigram extraction tool, the application of which is significant in natural language processing, together with a data analysis tool implemented using the pandas package.

# Installations
* Java 1.8.0_241
* Hadoop 3.1.3 : https://tinyurl.com/y9zqvsnp
* Mapreduce Java libraries: hadoop-core-0.20.0 and commons-cli-1.2 
* pandas 1.0.3 : https://pypi.org/project/pandas/

* Setup on EMR & S3: https://www.youtube.com/watch?v=JDk-LYJMzEU&t=19s

# Building blocks
* bigramCount.ipynb
* pandas.ipynb

# Testing
* Incremental testing when implement every new feature, no assumptions

# Guide (on local Windows machine)

### 1. Bigram Processing

Boot up Hadoop cluster
```bash
$ cd <sbin folder of Hadoop>
$ start-all.cmd
``` 
Check datanode, namenode, resource manager and nodemanager are up and running.


![boot_hadoop](./images/nodes.png)

Produce java executable & go to the folder of your .jar file to perform mapReduce
```bash
$ cd <folder with .jar file>
$ hadoop jar <jarFileName.jar> <packageName.ClassName>  <PathToInputTextFile> <PathToOutputDirectry>

To check results of <storageFolderOnHDFS>, which normally has its path as /user/<username>/<PathToOutputDirectry>
$ hadoop fs -ls <PathToOutputDirectry>
```

Sort and download the merged file.
```bash
$ hadoop fs -cat <PathToOutputDirectry>/part-r-* | sort > ./<localOutputFolder>/<combined.txt>
```
View number of bigrams OR number of lines since each line is designated for 1 bigrams
```bash
$ find /c /v "" "<localOutputFolder>/<combined.txt>"
```

A run-through example and instructions on deployment on cloud with Amazon Elastic MapReduce and S3 can be viewed in the [Report](https://github.com/KhaiTTNguyen/CIS_4517_DataIntensive_and_CloudComputing/tree/master/Project_5/Report) folder.

### 2. Pandas Analytics

All execution can be carried out in the [pandas.ipynb](https://github.com/KhaiTTNguyen/CIS_4517_DataIntensive_and_CloudComputing/blob/master/Project_5/pandas.ipynb) notebook.

# Issues
* Text processing issues, delimiters, regex
* Setting up Amazon EMR & S3
* Time management

# Further readings
* N-Grams statistics: https://openproceedings.org/2013/conf/edbt/BerberichB13.pdf
* N-gram language models: https://www.youtube.com/watch?v=GiyMGBuu45w

# Contribution
* Khai Nguyen (カイ∙グエン):  khainguyen@temple.edu