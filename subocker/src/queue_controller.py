#!/usr/bin/env python
import pika
import time
from .docker_controller import Docker
import os
import json

class QueueController:
    def __init__(self) -> None:
        print("Queue system: starting")
        credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), port=os.getenv('RABBITMQ_PORT'), credentials=credentials))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def run(self):
        print("Queue system: running")
        self.channel.basic_consume(queue='task_queue', on_message_callback=self.callback)
        self.channel.start_consuming()

    @staticmethod
    def set_environment(body: str) -> str:
        arg = json.loads(body)
        dir = "project-config/"
        path = os.path.join(dir, arg["project_name"])

        try:
            os.mkdir(path)
        except:
            print("Directory already exist")

        f = open(dir + arg["project_name"] + "/.env", "w")
        f.write("FILE_PATH="+ arg["path"])

        return dir + arg["project_name"] + "/.env"


    def callback(self, ch, method, properties, body):
        print("Queue system: received task")
        time.sleep(body.count(b'.'))

        print("Queue system: started new task")
        env_path = self.set_environment(body.decode('ascii'))
        docker = Docker(env_path=env_path)
        docker.run()
        print("Queue system: finished new task")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        docker.down()
        print("Queue system: sent task response")

