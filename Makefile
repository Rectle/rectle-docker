build: build-docker build-podman

build-docker: clean-docker
	docker-compose -f subocker/docker-compose.yml up --build --detach

build-podman: clean-podman
	podman-compose -f subman/podman-compose.yml up --build --detach

clean-docker:
	-docker container kill subocker-controller-1
	-docker container rm subocker-controller-1

clean-podman:
	-podman container kill subman_controller_1
	-podman container rm subman_controller_1

exec-docker:
	docker exec -ti subocker-controller-1 bash

exec-podman:
	podman exec -ti subman_controller_1 bash

.PHONY: build build-docker build-podman clean clean-docker clean-podman debug-docker debug-podman