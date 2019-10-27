#!/bin/bash

ID=$(hostname)-${USER//[^a-zA-Z0-9]/-}
IMAGE=mahjong_detector:1.12.0

exec docker run \
  -it \
  --runtime=nvidia \
  --hostname=$ID \
  --name=$ID \
  --publish-all \
  --volume /home:/home \
  $IMAGE \
  bash
