#!/bin/bash
cd subocker
docker compose up --build --detach

cd ../subman
podman build -t subman:1 .
podman container stop subman
podman container rm subman
podman run -ti --name=subman -p 42069:42069 -v ../volume:/app/volume subman:1