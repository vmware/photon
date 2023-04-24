---
title:  Configuration
weight: 3
---

To configure `photon-mgmtd`, use the `photon-mgmt.toml` file located in the following directory: `/etc/photon-mgmt/`

You can set values for the following keys in the `[System]` section:

`LogLevel=`  
Specifies the log level. The key takes one of the following:
values: `Trace`, `Debug`, `Info`, `Warning`, `Error`, `Fatal` and `Panic`. 
Default is `info`.

`UseAuthentication=`
Specifies whether a user needs authentication. This is a boolean key and takes the following values: `true`, `false`. 
Default is `true`.



You can set values for the following keys in the `[Network]` section:

`Listen=`
Specifies the IP address and port that the REST API server listens to.
When enabled, the default is `127.0.0.1:5208`.


`ListenUnixSocket=`
Specifies whether you want the server to listen on a unix domain socket `/run/photon-mgmt/photon-mgmt.sock`. This is a boolean key and takes the following values: `true`, `false`. 
Default is `true`.

**Note:** When you enable both `ListenUnixSocket=` and `Listen=`, server listens on the unix domain socket by default.

	❯ sudo cat /etc/photon-mgmt/photon-mgmt.toml                                     
	[System]
	LogLevel="info"
	UseAuthentication="false"
	
	[Network]
	ListenUnixSocket="true"


	❯ sudo systemctl status photon-mgmtd.service
	● photon-mgmtd.service - A REST API based configuration management microservice gateway
	     Loaded: loaded (/usr/lib/systemd/system/photon-mgmtd.service; disabled; vendor preset: disabled)
	     Active: active (running) since Thu 2022-01-06 16:32:19 IST; 4s ago
	   Main PID: 230041 (photon-mgmtd)
	      Tasks: 6 (limit: 15473)
	     Memory: 2.9M
	        CPU: 7ms
	     CGroup: /system.slice/photon-mgmtd.service
	             └─230041 /usr/bin/photon-mgmtd
	
	Jan 06 16:32:19 Zeus systemd[1]: photon-mgmtd.service: Passing 0 fds to service
	Jan 06 16:32:19 Zeus systemd[1]: photon-mgmtd.service: About to execute /usr/bin/photon-mgmtd
	Jan 06 16:32:19 Zeus systemd[1]: photon-mgmtd.service: Forked /usr/bin/photon-mgmtd as 230041
	Jan 06 16:32:19 Zeus systemd[1]: photon-mgmtd.service: Changed failed -> running
	Jan 06 16:32:19 Zeus systemd[1]: photon-mgmtd.service: Job 56328 photon-mgmtd.service/start finished, result=done
	Jan 06 16:32:19 Zeus systemd[1]: Started photon-mgmtd.service - A REST API based configuration management microservice gateway.
	Jan 06 16:32:19 Zeus systemd[230041]: photon-mgmtd.service: Executing: /usr/bin/photon-mgmtd
	Jan 06 16:32:19 Zeus photon-mgmtd[230041]: time="2022-01-06T16:32:19+05:30" level=info msg="photon-mgmtd: v0.1 (built go1.18beta1)"
	Jan 06 16:32:19 Zeus photon-mgmtd[230041]: time="2022-01-06T16:32:19+05:30" level=info msg="Starting photon-mgmtd... Listening on unix domain socket='/run/photon-mgmt/photon-mgmt.sock' in HTTP mode pid=103575">


## How to Configure Users?

### Unix domain socket

When you add users to the `photon-mgmt` group, they can access the unix socket.
Use the following command to add a user:  
	`# usermod -a -G photon-mgmt exampleusername`









        



