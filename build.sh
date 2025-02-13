#!/bin/bash

docker buildx build --platform linux/amd64 --provenance=false -t docker-image:tcg_scanner .
docker run --platform linux/amd64 -p 9000:8080 docker-image:tcg_scanner
