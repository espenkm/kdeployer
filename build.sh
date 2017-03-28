#!/usr/bin/env bash 

docker build -t espenkm/kdeployer:${TRAVIS_COMMIT:-latest} .
docker push espenkm/kdeployer:${TRAVIS_COMMIT:-latest}
