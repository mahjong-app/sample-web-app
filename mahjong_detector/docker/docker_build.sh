#!/bin/bash

IMAGE=mahjong_detector
VERSION=1.12.0

docker build -t $IMAGE:$VERSION .
