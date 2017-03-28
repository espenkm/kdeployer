#!/usr/bin/env bash 

COMMIT=${TRAVIS_COMMIT:-latest}
docker build -t espenkm/kdeployer:${COMMIT} .

docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
docker push espenkm/kdeployer:${COMMIT}
