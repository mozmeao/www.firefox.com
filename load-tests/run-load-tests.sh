#!/usr/bin/env bash

set -exo pipefail

docker run --rm -p 8089:8089 -v $PWD:/mnt/locust locustio/locust -f /mnt/locust/locustfile.py
