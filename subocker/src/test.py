from controllers.docker.main import Docker

docker = Docker()

for container in docker.get_containers():
    print(container)
docker.run()