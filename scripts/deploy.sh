#!/usr/bin/env bash 

COMMIT=${TRAVIS_COMMIT:-latest}
URL=${KDEPOYLER_SERVER:-kdeployer.local}

curl -i -H "Content-Type: application/json" \
    -X POST \
    -d @.kdeploy.yaml \
    -d '{"image": "espenkm/kdeployer:${COMMIT}"}' \
    http://${URL}/deploy