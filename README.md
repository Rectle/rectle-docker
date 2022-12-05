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
Update RabbitMQ configuration fields in `.env` file.
```
RABBITMQ_HOST="HOST ADDRESS HERE"
RABBITMQ_PORT="PORT HERE"
RABBITMQ_USER="USERNAME HERE"
RABBITMQ_PASS="PASSWORD HERE"
```

### Run

#### Application
```
python ./subocker/main.py
```
