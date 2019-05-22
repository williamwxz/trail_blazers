#!/bin/bash

docker stop airflow-webserver airflow-postgres
docker rm airflow-webserver airflow-postgres