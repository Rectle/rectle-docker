import pika
import time
import os
import shutil
import stat
import requests
import shutil
import json
import subprocess
from zipfile import ZipFile
from cloud_storage.cloud_storage_controller import CloudStorage


PODMAN_URL = "http://host.docker.internal:8082"


class QueueController:
    def __init__(self) -> None:
        print("Queue system: starting")
        self.channel = self.connect_to_rabbit()
        self.channel.queue_declare(queue="task_queue", durable=True)
        self.channel.basic_qos(prefetch_count=1)

    @staticmethod
    def connect_to_rabbit():
        while True:
            try:
                params = pika.URLParameters(os.getenv("RABBITMQ_URL"))
                connection = pika.BlockingConnection(params)
                channel = connection.channel()
                return channel
            except Exception as e:
                print("Failed to connect to RabbitMQ")
                print("Retring in 5s...")
                time.sleep(5)

    def run(self):
        print("Queue system: running")
        self.channel.basic_consume(
            queue="task_queue", on_message_callback=self.callback
        )
        self.channel.start_consuming()

    def prepare_project(self, project_id, model_id):
        path = "volume/project"

        if os.path.isdir(path):
            shutil.rmtree(path)

        os.makedirs(path, exist_ok=True)
        os.makedirs(path + "/gifs", exist_ok=True)

        simulation_src = f"projects/{project_id}/code.zip"
        raw_simulation_dest = "temp/code.zip"
        project_src = f"projects/{project_id}/models/{model_id}/model.zip"
        project_dest = path + "/model.zip"

        storage = CloudStorage()
        storage.import_file(simulation_src, raw_simulation_dest)
        storage.import_file(project_src, project_dest)

        zip_extractor = ZipFile(raw_simulation_dest, "r")
        zip_extractor.extractall(path="temp")
        zip_extractor = ZipFile(project_dest)
        zip_extractor.extractall(path=path)

        os.remove(raw_simulation_dest)
        os.remove(project_dest)
        main_dir = path + "/main.py"
        self.rectle_lib_hash("temp", path)

        os.chmod(main_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        # os.chmod(path + "/gifs", stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    @staticmethod
    def rectle_lib_hash(src_dir: str, dest_dir: str):
        command = ["python", "src/rectle_lib/build/lang/python.py", src_dir, dest_dir]
        subprocess.run(command)
        command = ["python", "src/rectle_lib/build/core.py", dest_dir]
        subprocess.run(command)

    @staticmethod
    def podman_healthcheck():
        url = PODMAN_URL + "/healthcheck"
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
    def send_to_podman(build_id):
        url = PODMAN_URL + f"/start_process/{build_id}"

        try:
            response = requests.get(url)
            print("Queue system: project executed")
            return response
        except Exception as e:
            print("Queue system: execution container failed")
            print(e)

    def callback(self, ch, method, properties, body):
        task = body.decode("ascii").replace("'", '"')
        task = json.loads(task)
        print("Queue system: received task")

        print(
            "Queue system: started new task {0}/{1}".format(
                task["projectId"], task["modelId"]
            )
        )
        self.prepare_project(task["projectId"], task["modelId"])

        print("Queue system: connecting to execution container")

        if self.podman_healthcheck_procedure():
            print("Queue system: sending project info")
            response = self.send_to_podman(task["compilationId"])

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
