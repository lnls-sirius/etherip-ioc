#!/bin/sh
set -exu

DOCKER_REGISTRY=dockerregistry.lnls-sirius.com.br
DOCKER_USER_GROUP=gas
DOCKER_IMAGE_PREFIX=${DOCKER_REGISTRY}/${DOCKER_USER_GROUP}

AUTHOR="Claudio F. Carneiro <claudiofcarneiro@hotmail.com>"
BRANCH=$(git branch --no-color --show-current)
BUILD_DATE=$(date -I)
BUILD_DATE_RFC339=$(date --rfc-3339=seconds)
COMMIT=$(git rev-parse --short HEAD)
DEPARTMENT=GAS
REPOSITORY=$(git remote show origin |grep Fetch|awk '{ print $3 }')
VENDOR="CNPEM"

BUILD_ENVS="\
    BRANCH=${BRANCH} \
    BUILD_DATE=${BUILD_DATE} \
    COMMIT_HASH=${COMMIT} \
    DEPARTMENT=${DEPARTMENT} \
    DOCKER_IMAGE_PREFIX=${DOCKER_IMAGE_PREFIX} \
    REPOSITORY=${REPOSITORY} \
    VENDOR=${VENDOR}"

if [ -f .env ]; then
    > .env
    echo AUTHOR=${AUTHOR} >> .env
    echo BUILD_DATE_RFC339=${BUILD_DATE_RFC339} >> .env
    for var in ${BUILD_ENVS}; do
        echo ${var} >> .env
    done
fi
