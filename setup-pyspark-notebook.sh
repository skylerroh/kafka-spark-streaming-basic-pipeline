#symlink w205 directory and open jupyter notebook on the spark container
docker-compose exec spark bash -c "ln -s /w205 w205"
docker-compose exec spark env PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port 8888 --ip 0.0.0.0 --allow-root' pyspark
