# Docker Containers

Photon OS includes the open source version of Docker. With Docker, Photon OS becomes a Linux run-time host for containers--that is, a Linux cloud container. A container is a process that runs on the Photon OS host with its own isolated application, file system, and networking.

On Photon OS, the Docker daemon is enabled by default. To view the status of the daemon, run this command: 

	systemctl status docker

Docker is loaded and running by default on the full version of Photon OS. On the minimal version, it is loaded but not running by default, so you have to start it: 

	systemctl start docker

To obtain information about Docker, run this command as root: 

	docker info

After you make sure that docker is enabled and started, you can, for example, run the following docker command as root to create a container running Ubuntu 14.04 with an interactive terminal shell: 

	docker run -i -t ubuntu:14.04 /bin/bash

Photon OS also enables you to run a docker container that, in turn, runs Photon OS: 

	docker run -i -t photon /bin/bash
