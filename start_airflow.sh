#!/bin/bash

img=`docker image ls | grep puckel/docker-airflow`
if [ ${#img} -eq 0 ]; then
    echo "Airflow docker image not found"
    docker pull puckel/docker-airflow
fi

echo "Starting airflow docker, based on directory: $(pwd)/plugins/"
docker run -d -p 8080:8080 -v $(pwd)/plugins/:/usr/local/airflow/plugins puckel/docker-airflow webserver