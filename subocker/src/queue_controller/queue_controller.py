import pika
import time
import os
import shutil
import stat
import requests
import shutil
import json
from zipfile import ZipFile
from cloud_storage.cloud_storage_controller import CloudStorage


PODMAN_URL = "http://host.docker.internal:8081" 


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


    def prepare_project(self, project_id, model_id):
        path = "volume/project" 

        if os.path.isdir(path):
            shutil.rmtree(path)
        
        os.makedirs(path, exist_ok = True)
        os.makedirs(path + '/gifs', exist_ok = True)
        
        simulation_src = f"projects/{project_id}/code.zip"
        simulation_dest = path + f"/code.zip"
        project_src = f"projects/{project_id}/models/{model_id}/model.zip"
        project_dest = path + f"/model.zip"

        storage = CloudStorage()
        storage.import_file(simulation_src, simulation_dest)
        storage.import_file(project_src, project_dest)

        zip_extractor = ZipFile(simulation_dest, 'r')
        zip_extractor.extractall(path=path)
        zip_extractor = ZipFile(project_dest)
        zip_extractor.extractall(path=path)

        os.remove(simulation_dest)
        os.remove(project_dest)

        os.chmod(path + '/main.py', stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        os.chmod(path + '/gifs', stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        

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
    def send_to_podman():
        url = PODMAN_URL + '/start_process'
        
        try:
            response = requests.get(url)
            print("Queue stystem: project executed")
            return response
        except Exception as e:
            print("Queue stystem: execution container failed")
            print(e)


    def callback(self, ch, method, properties, body):
        task = body.decode('ascii').replace("'", '"')
        task = json.loads(task)
        print("Queue system: received task")
        
        print("Queue system: started new task {0}/{1}".format(task['project_id'], task['model_id']))
        self.prepare_project(task['project_id'], task['model_id'])

        print("Queue system: connecting to execution container")
        
        if self.podman_healthcheck_procedure():
            print("Queue system: sending project info")
            response = self.send_to_podman()

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