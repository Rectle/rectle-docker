#!/usr/bin/env python
import pika
import time
from src.controllers.docker.main import Docker

class QueueController:
    def __init__(self) -> None:
        print("Queue system: starting")
        self.docker = Docker()
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
        
        print("Queue system: started new task")
        self.docker.run()
        print("Queue system: finished new task")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Queue system: sent task response")

