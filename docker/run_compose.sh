#!/bin/bash
echo "Starting Docker Compose..."
xhost +local:docker
docker compose run --rm stella-vslam-pc bash