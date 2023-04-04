import pika
import time
import os
import stat
import requests
import shutil
import subprocess
from requests.adapters import HTTPAdapter, Retry

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

    # @staticmethod
    # def set_environment(body: str) -> str:
    #     arg = json.loads(body)
    #     dir = "project-config/"
    #     path = os.path.join(dir, arg["project_name"])

    #     try:
    #         os.mkdir(path)
    #     except:
    #         print("Directory already exist")

    #     f = open(dir + arg["project_name"] + "/.env", "w")
    #     f.write("FILE_PATH="+ arg["path"])

    #     return dir + arg["project_name"] + "/.env"

    @staticmethod
    def prepare_project(project_name):
        path = "volume/" + project_name

        try:
            os.makedirs(path, exist_ok = True)
        except OSError as error:
            print("Directory '%s' can not be created" % path)

        shutil.copyfile('test-enviroments/CartPole/main.py', path + '/main.py')
        os.chmod(path + '/main.py', stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)


    def callback(self, ch, method, properties, body):
        print("Queue system: received task")
        
        time.sleep(3)
        print(body)

        print("Queue system: started new task")
        self. prepare_project(body.decode('ascii'))

        # TODO
        # - make bullet proof request sent + received msg
        # - add waiting for the response from podman container after everything is built or if error occured
        # - whole we have a http server maybe add additional end-points for error handling 
        url = 'http://host.docker.internal:42069/start_process/' + body.decode('ascii')
        try:
            response = requests.get(url)
            print(response.json)
        except Exception as e:
            print("Response failed")
            print(e)

        print("Queue system: finished new task")
        ch.basic_ack(delivery_tag=method.delivery_tag)

        print("Queue system: sent task response")