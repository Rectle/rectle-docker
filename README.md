# Rectle Docker
## Setup

### Requirements
- [docker](https://www.docker.com/)
- [docker compose](https://docs.docker.com/compose/)
- [podman](https://podman.io/)
- [podman compose](https://github.com/containers/podman-compose)
- [python:^3.8](https://www.python.org/)

### Installation
1. 
Create/update RabbitMQ configuration fields in `.env` file in `subocker/src` directory.

```
# example
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASS=guest
```

2.
Add Cloud Storage crudentials json file as `subocker_credentials.json` in `subocker/src` directory.

### Run

#### Docker
```
cd subocker/
docker compose up --build
```

#### Podman
```
cd subman/
podman_compose up --build
```

#### Swarm
##### Create service

Linux
```
docker service create \
    --name rectle \
    --mount 'type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock' \
    --replicas 10 \
    --update-delay 10s \
    --update-parallelism 2 \
    rectle-runner
```
Windows
```
docker service create --name rectle --mount 'type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock' --replicas 10 --update-delay 10s --update-parallelism 2 rectle-runner
```
##### Scale
```
docker service scale rectle=20
```

##### Remove
```
docker service remove rectle
```