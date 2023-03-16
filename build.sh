#!/bin/bash

docker build -f base.Dockerfile -t cluster-base:latest .

docker build -f spark-master.Dockerfile -t spark-master:latest .

docker build -f spark-worker.Dockerfile -t spark-worker:latest .