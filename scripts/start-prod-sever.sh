#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )/.."

echo "Building docker image"
nix build .#dockerImage

echo "Loading docker image"
output=$(docker load < result)
image_name=$(echo "$output" | grep -oP 'Loaded image: \K.*')

echo "Starting server from docker image: $image_name"
docker run --env-file backend/.env -e ETABETA_DATA_PATH=/chat_data -v $(pwd)/backend/chat_data:/chat_data  -p 8000:8000 --rm $image_name