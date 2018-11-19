# Docker Containers

On Photon OS, the Docker daemon is enabled by default. To view the status of the daemon, run the following command: 

	systemctl status docker

Docker is loaded and running by default on the full version of Photon OS. On the minimal version, it is loaded but not running by default. To tart it, run the following command: 

	systemctl start docker

To obtain information about Docker, run the following command as root: 

	docker info

After Docker is enabled and started, you can create a container. For eaxmple, run the following docker command as root to create a container running Ubuntu 14.04 with an interactive terminal shell: 

	docker run -i -t ubuntu:14.04 /bin/bash

Photon OS also enables you to run a docker container that runs Photon OS: 

	docker run -i -t photon /bin/bash
