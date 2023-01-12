#!/usr/bin/env python
import pika, time

class Publisher:
    def __init__(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)
        
    def run(self, text):
        self.channel.basic_publish(
            exchange="", 
            routing_key='task_queue', 
            body=str('{"path": "projects/test.py", "project_name": "test_project"}'), 
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

if __name__ == "__main__":
    publisher = Publisher()
    for i in range(5):
        publisher.run(i)
    publisher.connection.close()