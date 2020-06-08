#!/usr/bin/env bash
set -exo pipefail

: "${BASE_URL:=http://localhost:8080}"

urlwait "$BASE_URL"
py.test -n 2 --base-url "$BASE_URL" -v
