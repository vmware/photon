---
title:  Service Management
weight: 1
---

## POST Method ##

To manage the available services and take actions on the services, execute a POST request in the following format:

    curl --unix-socket  /run/photon-mgmt/photon-mgmt.sock  --request POST --data '{"action":"{command}”,”unit”:”{unit}"}' http://localhost/api/v1/service/systemd

The following table lists the parameters:

| Parameter      	| Description 	  |
| ----------- 	| ----------- |
| Unit      	| The name of the service you want to manage.|
| Action Commands | The action you want to take on the service. Start, stop, restart, try-restart, reload-or-restart, reload, enable, disable, mask, unnmask, kill        |


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request POST --data '{"action":"start","unit":"nginx.service"}' http://localhost/api/v1/service/systemd

**Response:** 
 
	{
	   "success":true,
	   "message":"",
	   "errors":""
	}


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request POST --data '{"action":"stop","unit":"nginx.service"}' http://localhost/api/v1/service/systemd

**Response:**  

	{
	   "success":true,
	   "message":"",
	   "errors":""
	}


## GET Method: ##

### Status of all the services: ###
The `systemctl list-unit-files` command lists all the services available in the system. 
To fetch the list of services listed in the list-unit files, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/units

Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/units
 


### Status of a Specific Service: ###

To receive the status details of a specific service, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/{unit}/status

The following table lists the parameter:

|Parameter	| Description	|
|-----------|---------------|
|Unit		|The name of the service for which you want to get the status.|


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost:5208/api/v1/service/systemd/nginx.service/status | jq	% Total % Received % Xferd Average Speed Time Time Time Current	Dload Upload Total Spent Left Speed	100 514 100 514 0 0 38298 0 --:--:-- --:--:-- --:--:-- 39538

**Response**:  
    
	{
	   "success":true,
	   "message":{
	      "Property":"inactive",
	      "Unit":"nginx.service",
	      "Name":"nginx.service",
	      "Description":"Nginx High-performance HTTP server and reverse proxy",
	      "MainPid":0,
	      "LoadState":"loaded",
	      "ActiveState":"inactive",
	      "SubState":"dead",
	      "Followed":"",
	      "Path":"/org/freedesktop/systemd1/unit/nginx_2eservice",
	      "JobId":0,
	      "JobType":"",
	      "JobPath":"/",
	      "UnitFileState":"disabled",
	      "StateChangeTimestamp":0,
	      "InactiveExitTimestamp":0,
	      "ActiveEnterTimestamp":0,
	      "ActiveExitTimestamp":0,
	      "InactiveEnterTimestamp":0
	   },
	   "errors":""
	}


### Value of a Specific Property ###

To fetch the value of a specific property, execute a GET request in the following format:

	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/manager/property/Version


The following table lists the parameter:

|Parameter	| Description	|
|-----------|---------------|
|Property		|Version, Features, Virtualization, Architecture, Tainted.|


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://127.0.0.1/api/v1/service/systemd/manager/property/Virtualization

**Response:**  
    
	{
	   "success":true,
	   "message":{
	      "property":"Virtualization",
	      "value":"vmware"
	   },
	   "errors":""
	}


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://127.0.0.1/api/v1/service/systemd/manager/property/Architecture

**Response:**  
    
	{
	   "success":true,
	   "message":{
	      "property":"Architecture",
	      "value":"x86-64"
	   },
	   "errors":""
	}


### Properties of a Specific Service ###

To fetch the property of a specific service, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/{unit}/property


The following table lists the parameter:

|Parameter	| Description	|
|-----------|---------------|
|Unit		|The name of the service for which you want to get the properties.|


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/nginx.service/property


### Properties of All Services ###

To fetch all the properties of a service, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/{unit}/propertyall

The following table lists the parameter:

|Parameter	| Description	|
|-----------|---------------|
|Unit		|The name of the service for which you want to fetch the properties.|


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/nginx.service/propertyall | jq % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 100 9652 0 9652 0 0 1058k 0 --:--:-- --:--:-- --:--:-- 1178k



### Configuration Details ###

To receive the configuration details, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/conf

Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/conf

**Response:**  
    
	{
	   "success":true,
	   "message":{
	      "CPUAffinity":"",
	      "CapabilityBoundingSe":"",
	      "CrashChangeVT":"",
	      "CrashReboot":"",
	      "CrashShell":"",
	      "CtrlAltDelBurstAction":"",
	      "DefaultBlockIOAccounting":"",
	      "DefaultCPUAccounting":"",
	      "DefaultEnvironment":"",
	      "DefaultIOAccounting":"",
	      "DefaultIPAccounting":"",
	      "DefaultLimitAS":"",
	      "DefaultLimitCORE":"",
	      "DefaultLimitCPU":"",
	      "DefaultLimitDATA":"",
	      "DefaultLimitFSIZE":"",
	      "DefaultLimitLOCKS":"",
	      "DefaultLimitMEMLOCK":"",
	      "DefaultLimitMSGQUEUE":"",
	      "DefaultLimitNICE":"",
	      "DefaultLimitNOFILE":"",
	      "DefaultLimitNPROC":"",
	      "DefaultLimitRSS":"",
	      "DefaultLimitRTPRIO":"",
	      "DefaultLimitRTTIME":"",
	      "DefaultLimitSIGPENDING":"",
	      "DefaultLimitSTACK":"",
	      "DefaultMemoryAccounting":"",
	      "DefaultRestartSec":"",
	      "DefaultStandardError":"",
	      "DefaultStandardOutput":"",
	      "DefaultStartLimitBurst":"",
	      "DefaultStartLimitIntervalSec":"",
	      "DefaultTasksAccounting":"",
	      "DefaultTasksMax":"",
	      "DefaultTimeoutStartSec":"",
	      "DefaultTimeoutStopSec":"",
	      "DefaultTimerAccuracySec":"",
	      "DumpCore":"",
	      "IPAddressAllow":"",
	      "IPAddressDeny":"",
	      "JoinControllers":"",
	      "LogColor":"",
	      "LogLevel":"",
	      "LogLocation":"",
	      "LogTarget":"",
	      "RuntimeWatchdogSec":"",
	      "ShowStatus":"",
	      "ShutdownWatchdogSec":"",
	      "SystemCallArchitectures":"",
	      "TimerSlackNSec":""
	   },
	   "errors":""
	}


### Configuration Update Details ###

To fetch the details about the configuration updates, execute a GET request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/conf/update

Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock http://localhost/api/v1/service/systemd/conf/update

**Response:**  
    
	{
	   "success":true,
	   "message":{
	      "CPUAffinity":"",
	      "CapabilityBoundingSe":"",
	      "CrashChangeVT":"",
	      "CrashReboot":"",
	      "CrashShell":"",
	      "CtrlAltDelBurstAction":"",
	      "DefaultBlockIOAccounting":"",
	      "DefaultCPUAccounting":"",
	      "DefaultEnvironment":"",
	      "DefaultIOAccounting":"",
	      "DefaultIPAccounting":"",
	      "DefaultLimitAS":"",
	      "DefaultLimitCORE":"",
	      "DefaultLimitCPU":"",
	      "DefaultLimitDATA":"",
	      "DefaultLimitFSIZE":"",
	      "DefaultLimitLOCKS":"",
	      "DefaultLimitMEMLOCK":"",
	      "DefaultLimitMSGQUEUE":"",
	      "DefaultLimitNICE":"",
	      "DefaultLimitNOFILE":"",
	      "DefaultLimitNPROC":"",
	      "DefaultLimitRSS":"",
	      "DefaultLimitRTPRIO":"",
	      "DefaultLimitRTTIME":"",
	      "DefaultLimitSIGPENDING":"",
	      "DefaultLimitSTACK":"",
	      "DefaultMemoryAccounting":"",
	      "DefaultRestartSec":"",
	      "DefaultStandardError":"",
	      "DefaultStandardOutput":"",
	      "DefaultStartLimitBurst":"",
	      "DefaultStartLimitIntervalSec":"",
	      "DefaultTasksAccounting":"",
	      "DefaultTasksMax":"",
	      "DefaultTimeoutStartSec":"",
	      "DefaultTimeoutStopSec":"",
	      "DefaultTimerAccuracySec":"",
	      "DumpCore":"",
	      "IPAddressAllow":"",
	      "IPAddressDeny":"",
	      "JoinControllers":"",
	      "LogColor":"",
	      "LogLevel":"",
	      "LogLocation":"",
	      "LogTarget":"",
	      "RuntimeWatchdogSec":"",
	      "ShowStatus":"",
	      "ShutdownWatchdogSec":"",
	      "SystemCallArchitectures":"",
	      "TimerSlackNSec":""
	   },
	   "errors":""
	}




