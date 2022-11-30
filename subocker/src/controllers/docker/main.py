from python_on_whales import docker
import datetime

class Docker:
    def __init__(self) -> None:
        pass

    def get_containers(self) -> list:
        return []

    def run(self) -> bool:
        timestamp = docker.system.info().system_time
        docker.compose.up(detach=True, build=False)

        for (_, line) in docker.compose.logs(stream=True, follow=True, timestamps =True, since=timestamp):
            print(str(line))

        return True
