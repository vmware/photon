---
title:  Docker Rootless Support
weight: 1.1
---

## Run the Docker daemon as a non-root user (Rootless mode)

The Rootless mode allows you to run the Docker daemon and containers as a non-root user. This mitigates the potential vulnerabilities in the daemon and the container runtime.

 As long as the prerequisites are met, rootless mode does not require root privileges even during the installation of the Docker daemon.


After its introduction in Docker Engine v19.03 as an experimental feature, the rootless mode was available in Docker Engine v20.10 as a more stable feature.

This feature is available in Photon OS 4.0 and above versions starting from the docker-20.10.14-1 version (in Ph4).

### Prerequisites:

- You must install `newuidmap` and `newgidmap` on the host. - Provided by the `shadow` package in Photon

- `/etc/subuid` and `/etc/subgid` should contain at least 65,536 subordinate UIDs/GIDs for the user. In the following example, the user called `testuser` has 65,536 subordinate UIDs/GIDs (100000-165535).

- You can install the pre-required packages using the following command: 
	
	```
	tdnf install -y shadow fuse slirp4netns libslirp
	```    

- Photon 3 or above with docker-20.10.14-1 version (this version is specific to Ph4. For higher versions please refer spec file in the Photon source).


### Usage:

You can perform the following tasks with the respective commands for them:

1. Install docker-rootless using the following command:  

	```
	tdnf install -y docker-rootless
	```   

2. Use the following command to add a new user: 
	```
	useradd -m test_user
	```   
3. Use the following command to set a password for the new user: 
	```
	passwd test_user
	```   
4. Use the following command to log in as the user you created: 
	```
	`ssh test_user@localhost`
	```   

5. Run the following command: 

	```
	dockerd-rootless-setuptool.sh --help`
	```   
	The above command shows something like the following output:

	``` 
	test_user@photon [ ~ ]$ dockerd-rootless-setuptool.sh --help
	Usage: /usr/bin/dockerd-rootless-setuptool.sh [OPTIONS] COMMAND
	 
	A setup tool for Rootless Docker (dockerd-rootless.sh).
	 
	Documentation: https://docs.docker.com/go/rootless/
	 
	Options:
	-f, --force Ignore rootful Docker (/var/run/docker.sock)
	--skip-iptables Ignore missing iptables
	 
	Commands:
	check Check prerequisites
	install Install systemd unit (if systemd is available) and show how to manage the service
	uninstall Uninstall systemd unit
	```    


6. Run the following command, and then check and fix the errors and warnings, if any:
	```
	dockerd-rootless-setuptool.sh`
	```   
	Run the following commands:

	a. `echo "test_user:100000:65536" >> /etc/subuid`

	b. `echo "test_user:100000:65536" >> /etc/subgid`

	c. `echo "kernel.unprivileged_userns_clone = 1" >> /etc/sysctl.d/50-rootless.conf`

	d. `chmod 644 /etc/subuid /etc/subgid /etc/sysctl.d/50-rootless.conf`

	e. `sysctl --system`
	
	After you run the above commands, the `dockerd-rootless-setuptool.sh check` shows the following output:
	
	```
	test_user@photon [ ~ ]$ dockerd-rootless-setuptool.sh check
	 
	[INFO] Requirements are satisfied
	```   

7. After the `Requirements are satisfied` message appears,  run the following command: 

	```
	dockerd-rootless-setuptool.sh install
	```   

8. Carefully, go through the output messages of the above command and ensure that everything is fine. Follow the instructions that appear, if any.

9. Add the following to your `.bashrc` or `.bash_profile`:

	```
	export PATH=/usr/bin:$PATH
	export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock
	```   
Now, you can run `docker run -it photon` as a regular user.


### Limitations:

**Exposing Network Ports**
Be aware that port numbers below 1024 are called privileged ports and are not available for rootless users. So, you need to use the unprivileged ports such as  8080, and so on. If you want to run an HTTP server, you need to run `docker run -p 8080:80`. However, if you really need to expose privileged ports, you can do that by adjusting `sysctl /proc/sys/net/ipv4/ip_unprivileged_port_start` or by setting `CAP_NET_BIND SERVICE` capability on the binary rootlesskit.

**Limiting Resources such as CPU, Memory**

Limiting resources with cgroup-related `docker run` flags such as `--cpus`, `--memory`, `--pids-limit` is supported only while running with cgroup v2 and systemd.

If `docker info` shows `none` as `Cgroup Driver`, the conditions are not satisfied. When these conditions are not satisfied, rootless mode ignores the cgroup-related `docker run` flags.

