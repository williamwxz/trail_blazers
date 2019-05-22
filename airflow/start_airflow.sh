#!/bin/bash

echo "Starting airflow docker" 
echo "Mount $(pwd)/plugins/ and $(pwd)/dags/"

docker-compose up -d
