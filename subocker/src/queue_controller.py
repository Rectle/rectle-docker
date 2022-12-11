#!/usr/bin/env python
import pika
import time
from src.controllers.docker.main import Docker
from .cloud_store import CloudStore
import os

class QueueController:
    def __init__(self) -> None:
        print("Queue system: starting")
        self.docker = Docker()
        print(os.getenv('RABBITMQ_PASS'))
        credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'), port=os.getenv('RABBITMQ_PORT'), credentials=credentials))
        self.cloudstore = CloudStore("subocker/rectle-platform-63c7ef33e4e4.json", "subocker-projects")
        self.channel = connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def run(self):
        print("Queue system: running")
        self.channel.basic_consume(queue='task_queue', on_message_callback=self.callback)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print("Queue system: received task")
        # print(ch, method, body)
        time.sleep(body.count(b'.'))
        self.cloudstore.download_and_unzip("projectFiles/project1.zip", "runtime-enviroment/src/", "code.zip")
        print("Queue system: file downloaded")
        print("Queue system: started new task")
        self.docker.run()
        print("Queue system: finished new task")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Queue system: sent task response")

