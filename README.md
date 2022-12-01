# Rectle Docker
## Setup

### Requirements
- [docker](https://www.docker.com/)
- [python:^3.8](https://www.python.org/)

### Installation

```
pip install -r ./subocker/requirements.txt
```

### Run

#### RabbitMQ
```
cd rabbitmq
docker compose up
cd ..
```

#### Application
```
python ./subocker/main.py
```
