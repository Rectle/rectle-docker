from python_on_whales import DockerClient
from uuid import uuid4

class Docker:
    def __init__(self, uuid: str = None) -> None:
        project_name = f'rectle-docker-{uuid if uuid is not None else str(uuid4())}'
        self.docker = DockerClient(compose_project_name=project_name, compose_project_directory=None)

    def get_containers(self) -> list:
        return []

    def run(self) -> bool:
        timestamp = self.docker.system.info().system_time
        self.docker.compose.up(detach=True, build=False)

        for (_, line) in self.docker.compose.logs(stream=True, follow=True, timestamps =True, since=timestamp):
            # TODO send logs to the server
            print(str(line))

        return True
