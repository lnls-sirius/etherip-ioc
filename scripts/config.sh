#!/bin/sh
set -exu

DOCKER_REGISTRY=dockerregistry.lnls-sirius.com.br
DOCKER_USER_GROUP=gas
DOCKER_IMAGE_PREFIX=${DOCKER_REGISTRY}/${DOCKER_USER_GROUP}

cat << EOF > .env
AUTHOR=Claudio F. Carneiro
MAINTAINER=Rafael B. Cardoso
BRANCH=$(git branch --no-color --show-current)
BUILD_DATE=$(date -I)
BUILD_DATE_RFC339=$(date --rfc-3339=seconds)
COMMIT_HASH=$(git rev-parse --short HEAD)
DEPARTMENT=GAS
DOCKER_IMAGE_PREFIX=${DOCKER_IMAGE_PREFIX}
REPOSITORY=$(git remote show origin |grep Fetch|awk '{ print $3 }')
VENDOR=CNPEM
EOF
