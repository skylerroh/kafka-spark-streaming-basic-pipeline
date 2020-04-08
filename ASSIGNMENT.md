# Project 3: Understading User Behavior
## Setting up the cluster
Cluster setup is documented and scripted in `startup.sh`
The startup script is commented with the following steps:  
1. bring up the cluster with docker-compose up -d
2. try to create the kafka topic `events`, if the cluster is still coming up, try again after 5 seconds
3. describe the created events topic
4. install redis and numpy for python2 in mids container (for the game_api and scripting the test events with random values)
5. start flask

### Cluster components
The cluster that is setup with `docker-compose.yml` is composed of 6 containers:  
1. zookeeper
2. kafka
3. spark
4. mids-base
5. redis
6. cloudera


## Set up pyspark notebook
Pyspark notebook setup is scripted in `setup-pyspark-notebook.sh` and contains two steps
1. symlink w205 directory
2. open jupyter notebook on the spark container and expose on port 8888
  

## Run the pipeline
Once set up,
1. the streaming process needs to be started within the notebook `SparkStreamingAndAnalysis.ipynp`
2. run `create_test_events.py` within the mids container to launch randomized apache bench commands with `docker-compose exec mids python /w205/project-3-skylerroh/create_test_events.py`
3. the apache bench commands hit the flask app endpoints, which write logs to kafka of various events including buying/selling inventory and joining/leaving guilds
    - user state is tracked for these actions with redis
4. the events written to karka by flask app are consumed by spark streaming every 10 sec, split by event_type and written to hdfs
4. stop the sparkstreaming process with keyboard interrupt
5. analyze the parquet files written out by the streaming process in the pyspark notebook 

