#symlink w205 directory and open jupyter notebook on the spark container
docker-compose exec spark bash -c "ln -s /w205 w205"
docker-compose exec spark env PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port 8888 --ip 0.0.0.0 --allow-root' pyspark --jars /w205/spark-redis/target/spark-redis_2.11-2.4.3-SNAPSHOT-jar-with-dependencies.jar –conf "spark.redis.host=redis" –conf "spark.redis.port=6379"
