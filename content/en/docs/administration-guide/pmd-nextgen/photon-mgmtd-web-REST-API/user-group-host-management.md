---
title:  User, Group, and Host Management
weight: 4
---

## POST Method ##

### Add a Group ###

To add a group, execute a POST request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request POST --data '{"Name":"photon","Gid":"1125"}' http://localhost/api/v1/system/group/add

The following table lists the parameter:

|Parameter	| Description	|
|-----------|---------------|
|Gid		|ID of the group that you want to add.|
|Name 		|Name of the group that you want to add.|

Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request POST --data '{"Name":"photon","Gid":"1125"}' http://localhost/api/v1/system/group/add

**Response:**  
    
	{
	   "success":true,
	   "message":"group added",
	   "errors":""
	}


### Add a User ###

To add a user, execute a POST request in the following format:

	curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request POST --data '{"Name":"photon1"}' http://localhost/api/v1/system/user/add

The following table lists the parameter:

|Parameter	| Description	|
|-----------|---------------|
|Name 		|Name of the user you want to add.|


Example: 
	
	curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request POST --data '{"Name":"photon1"}' http://localhost/api/v1/system/user/add


## DELETE Method ##

### Remove a Group ###

To remove a group, execute a DELETE request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request DELETE --data '{"Name":"photon","Gid":"1125"}' http://localhost/api/v1/system/group/remove

The following table lists the parameters:

| Parameter      	| Description 	  |
| ----------- 	| ----------- |
|Name      	|Name of the group you want to delete.|
|Gid			|ID of the group that you want to delete.| 


Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request DELETE --data '{"Name":"photon22"}' http://localhost/api/v1/system/group/remove

**Response:**  
	
	{
	   "success":true,
	   "message":"group removed",
	   "errors":""
	}



### Remove a User ###

To remove a user, execute a DELETE request in the following format:

	curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request DELETE --data '{"Name":"photon1"}' http://localhost/api/v1/system/user/remove

**Response**

	{
	   "success":true,
	   "message":"user removed",
	   "errors":""
	}


## PUT Method ##

### Modify Group ###

To modify the name of a group, execute a PUT request in the following format:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request PUT --data '{"Name":"photon6","NewName":"photon33"}' http://localhost/api/v1/system/group/modify


Example:

    curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request PUT --data '{"Name":"photon6","NewName":"photon33"}' http://localhost/api/v1/system/group/modify


## GET Method ##

### Host Details ###

To fetch the details of the host, execute a GET request in the following format:

	curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request GET http://localhost/api/v1/system/hostname/describe


Example: 
	
	curl --unix-socket /run/photon-mgmtd/photon-mgmtd.sock --request GET http://localhost/api/v1/system/hostname/describe | jq % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 100 585 100 585 0 0 8374 0 --:--:-- --:--:-- --:--:-- 8478