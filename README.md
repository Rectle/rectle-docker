# Rectle Docker
## Setup

### Requirements
- [docker](https://www.docker.com/)
- [python:^3.8](https://www.python.org/)

### Installation

1. Install dependecies
```
pip install -r ./subocker/requirements.txt
```

2. 
Create/update RabbitMQ configuration fields in `.env` file in `subocker` directory.

```
# example
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASS=guest
```

### Build
```
docker build . -t rectle-runner
```

### Run

#### Local
```
python subocker/main.py
```

#### Docker
```
docker run --restart always -v /var/run/docker.sock:/var/run/docker.sock -d --name rectle rectle-runner
```

#### Swarm
##### Create service

Linux
```
docker service create \
    --name rectle \
    --replicas 10 \
    --rollback \
    --update-delay 10s \
    --update-parallelism 2 \
    rectle-runner
```
Windows
```
docker service create --name rectle --replicas 10 --rollback --update-delay 10s --update-parallelism 2 rectle-runner
```

##### Remove
```
docker service remove rectle
```