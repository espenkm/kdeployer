#!/usr/bin/env bash 

DATE=`date '+%Y%m%d%H%M%S'`
docker build -t espenkm/kdeployer:${DATE} -t espenkm/kdeployer:latest ..

#docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
docker push espenkm/kdeployer:latest
docker push espenkm/kdeployer:${DATE}
