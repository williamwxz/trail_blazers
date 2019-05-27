#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "$0 [bash|airflow [list_dag|...]]"
    exit 1
fi

docker run --rm -ti puckel/docker-airflow $1