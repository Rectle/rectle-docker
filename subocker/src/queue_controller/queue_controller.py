import pika
import time
import os
import stat
import requests
import shutil
import subprocess
from requests.adapters import HTTPAdapter, Retry
from httpserver.httpserver import Server

class QueueController:
    def __init__(self) -> None:
        print("Queue system: starting")
        self.channel = self.connect_to_rabbit()
        self.channel.queue_declare(queue='task_queue', durable=True)
        self.channel.basic_qos(prefetch_count=1)


    @staticmethod
    def connect_to_rabbit():
        while True:
            try:
                credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
                connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=os.getenv('RABBITMQ_HOST'), 
                    port=os.getenv('RABBITMQ_PORT'), 
                    credentials=credentials))
                channel = connection.channel()
                return channel
            except Exception as e:
                print("Failed to connect to RabbitMQ")
                print("Retring in 5s...")
                time.sleep(5)


    def run(self):
        print("Queue system: running")
        self.channel.basic_consume(queue='task_queue', on_message_callback=self.callback)
        self.channel.start_consuming()


    @staticmethod
    def prepare_project(project_name):
        path = "volume/" + project_name

        try:
            os.makedirs(path, exist_ok = True)
        except OSError as error:
            print("Directory '%s' can not be created" % path)

        shutil.copyfile('test-enviroments/CartPole/main.py', path + '/main.py')
        os.chmod(path + '/main.py', stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)


    @staticmethod
    def send_to_podman(project_name):
        url = 'http://host.docker.internal:42069/start_process/' + project_name

        try:
            response = requests.get(url)
            print(response.json)
            print("Queue stystem: Enviroment is being built")
        except Exception as e:
            print("Response failed")
            print(e)


    def callback(self, ch, method, properties, body):
        project_name = body.decode('ascii')

        print("Queue system: received task")
        
        time.sleep(3)
        print(body)

        print("Queue system: started new task")
        self.prepare_project(project_name)

        # TODO
        # - make bullet proof request sent + received msg
        # - add waiting for the response from podman container after everything is built or if error occured
        self.send_to_podman(project_name)

        print("Queue system: finished new task")

        ch.basic_ack(delivery_tag=method.delivery_tag)

        print("Queue system: sent task response")