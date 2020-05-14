#!/bin/bash
set -ex

DOCKER_IMAGE="mozmeao/www.firefox.com:${CI_COMMIT_SHORT_SHA}"
DOCKER_IMAGE_LATEST="mozmeao/www.firefox.com:latest"
DOCKER_TEST_IMAGE="mozmeao/www.firefox.com:tests-${CI_COMMIT_SHORT_SHA}"
DOCKER_TEST_IMAGE_LATEST="mozmeao/www.firefox.com:tests-latest"

if docker pull "$DOCKER_IMAGE"; then
    # image already exists, skip the build and push
    exit 0
fi

make build

# push git tagged images
make push

# push latest image
docker tag "$DOCKER_IMAGE" "$DOCKER_IMAGE_LATEST"
docker push "$DOCKER_IMAGE_LATEST"

# push latest tests image
docker tag "$DOCKER_TEST_IMAGE" "$DOCKER_TEST_IMAGE_LATEST"
docker push "$DOCKER_TEST_IMAGE_LATEST"
