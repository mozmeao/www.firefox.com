#!/bin/bash

set -ex

kubectl create namespace "$NS" || true
