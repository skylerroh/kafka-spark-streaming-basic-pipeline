# Project 3: Understading User Behavior
## Setting up the cluster
Cluster setup is documented and scripted in `startup.sh`
The startup script is commented with the following steps:  
1. bring up the cluster with docker-compose up -d
2. try to create the kafka topic `events`, if the cluster is still coming up, try again after 5 seconds
3. describe the created events topic
4. start flask in background
5. symlink w205 directory and open jupyter notebook on the spark container

6. check that 3280 messages are on the topic
7. symlink w205 directory and open jupyter notebook on the spark container
  
The cluster that is setup with `docker-compose.yml` is composed of 4 containers:  
1. zookeeper
2. kafka
3. spark
4. mids-base
  
Once the cluster comes up, pyspark is run via a jupyter notebook hosted on port 8888
## Steps
`bash startup.sh`
connect to jupyter notebook running on spark container and start streaming
`docker-compose exec mids bash -c "bash /w205/project-3-skylerroh/test_events.sh"`
