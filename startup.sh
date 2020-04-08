# bring up cluster
docker-compose up -d

# try to create the kafka topic, if the cluster is still coming up, try again after 5 seconds
n=0
until [ $n -ge 5 ]
do
    docker-compose exec kafka kafka-topics --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181 && break
    echo "Unable to create Kafka topic 'events’, trying again"
    n=$[$n+1]
    sleep 5
done

# describe the created assessments topic
docker-compose exec kafka kafka-topics --describe --topic events  --zookeeper zookeeper:32181

# installing redis for py2 on mids container
docker-compose exec mids pip install -U redis
docker-compose exec mids pip install -U numpy==1.16.5

# run Flask
echo "starting flask"
docker-compose exec mids env FLASK_APP=/w205/project-3-skylerroh/game_api.py flask run --host 0.0.0.0
