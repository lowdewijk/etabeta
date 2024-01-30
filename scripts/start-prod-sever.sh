#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )/.."
nix build .#dockerImage
output=$(docker load < result)
image_name=$(echo "$output" | grep -oP 'Loaded image: \K.*')
docker run --env-file backend/.env -e ETABETA_DATA_PATH=/chat_data -v $(pwd)/backend/chat_data:/chat_data  -p 8000:8000 --rm $image_name