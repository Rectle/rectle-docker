import pika
import time
import os
import stat
import requests
import shutil
import subprocess
from requests.adapters import HTTPAdapter, Retry
from httpserver.httpserver import Server
from zipfile import ZipFile


PODMAN_URL = "http://host.docker.internal:42069" 


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
            os.makedirs(path + '/gifs', exist_ok = True)
        except OSError as error:
            print("Directory '%s' can not be created" % path)

        path += '/'

        shutil.copyfile('test-enviroments/CartPole/CartPole_simulation.zip', path + 'CartPole_simulation.zip')
        shutil.copyfile(f'test-enviroments/CartPole/{project_name}/trained_model.zip', path + 'trained_model.zip')
        zip_extractor = ZipFile(path + '/CartPole_simulation.zip', 'r')
        zip_extractor.extractall(path=path)
        zip_extractor = ZipFile(path + '/trained_model.zip')
        zip_extractor.extractall(path=path)

        os.chmod(path + 'main.py', stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        os.chmod(path + 'gifs', stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)


    @staticmethod
    def podman_healthcheck():
        url = PODMAN_URL + '/healthcheck'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except Exception as e:
            print("Podman container failed healthcheck")
            
        return False

    
    def podman_healthcheck_procedure(self, time_in_sec=30, check_delay=10):
        tries = int(time_in_sec / check_delay)
        for t in range(tries):
            print(f"Podman container: Try {t + 1}/{tries}")
            if self.podman_healthcheck():
                return True
            else:
                time.sleep(check_delay)

        print("Podman container: Container unreachable")
        return False


    @staticmethod
    def send_to_podman(project_name):
        url = PODMAN_URL + '/start_process/' + project_name
        
        try:
            response = requests.get(url)
            print("Queue stystem: project executed")
            return response
        except Exception as e:
            print("Queue stystem: execution container failed")
            print(e)


    def callback(self, ch, method, properties, body):
        project_name = body.decode('ascii')

        print("Queue system: received task")
        
        time.sleep(3)
        print(body)

        print("Queue system: started new task")
        self.prepare_project(project_name)

        print("Queue system: connecting to execution container")
        
        if self.podman_healthcheck_procedure():
            print("Queue system: sending project info")
            response = self.send_to_podman(project_name)

            if response.status_code == 200:
                print("Queue system: finished new task")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print("Queue system: sent task response")
            else:
                print("Queue system: task execution failed")
        else:
            print("Queue system: Task failed")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            print("Queue system: Sending task back to the queue")