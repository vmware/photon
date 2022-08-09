---
title:  User, Group, and Host Management
weight: 4
---

## POST Method ##

### Add a Group ###

To add a group, execute a POST request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request POST --data '{"Name":"photon","Gid":"1125"}' http://localhost/api/v1/system/group/add

The following table lists the parameter:

|Parameter	| Description	|
|-----------|---------------|
|Gid		|ID of the group that you want to add.|
|Name 		|Name of the group that you want to add.|

Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request POST --data '{"Name":"photon","Gid":"1125"}' http://localhost/api/v1/system/group/add

**Response:**  
    
	{
	   "success":true,
	   "message":"group added",
	   "errors":""
	}


### Add a User ###

To add a user, execute a POST request in the following format:

	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request POST --data '{"Name":"photon1"}' http://localhost/api/v1/system/user/add

The following table lists the parameter:

|Parameter	| Description	|
|-----------|---------------|
|Name 		|Name of the user you want to add.|


Example: 
	
	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request POST --data '{"Name":"photon1"}' http://localhost/api/v1/system/user/add


## DELETE Method ##

### Remove a Group ###

To remove a group, execute a DELETE request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request DELETE --data '{"Name":"photon","Gid":"1125"}' http://localhost/api/v1/system/group/remove

The following table lists the parameters:

| Parameter      	| Description 	  |
| ----------- 	| ----------- |
|Name      	|Name of the group you want to delete.|
|Gid			|ID of the group that you want to delete.| 


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request DELETE --data '{"Name":"photon22"}' http://localhost/api/v1/system/group/remove

**Response:**  
	
	{
	   "success":true,
	   "message":"group removed",
	   "errors":""
	}



### Remove a User ###

To remove a user, execute a DELETE request in the following format:

	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request DELETE --data '{"Name":"photon1"}' http://localhost/api/v1/system/user/remove

**Response**

	{
	   "success":true,
	   "message":"user removed",
	   "errors":""
	}


## PUT Method ##

### Modify Group ###

To modify the name of a group, execute a PUT request in the following format:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request PUT --data '{"Name":"photon6","NewName":"photon33"}' http://localhost/api/v1/system/group/modify


Example:

    curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request PUT --data '{"Name":"photon6","NewName":"photon33"}' http://localhost/api/v1/system/group/modify


## GET Method ##

### Host Details ###

To fetch the details of the host, execute a GET request in the following format:

	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request GET http://localhost/api/v1/system/hostname/describe


Example: 
	
	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request GET http://localhost/api/v1/system/hostname/describe | jq % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 100 585 100 585 0 0 8374 0 --:--:-- --:--:-- --:--:-- 8478


## Login Status ##

You can use the `pmctl` tool to get login details of users. The following section lists the commands you can use to get the user details.


#### List Users

To list all the logged in users, use the following command in the `pmctl` tool:

	>pmctl status login user

#### List Sessions

To list all the logged in sessions, use the following command in the `pmctl` tool:

	>pmctl status login session

#### Get User based on UID

To get the status of users based on user ID, use `pmctl` command in the following format:

	pmctl status login user <UID>

Example: 
	
	>pmctl status login user 2

#### Get Session based on ID

To get the status of logged in sessions based on the users ID, use the `pmctl` command in the following format:

	pmctl status login session <ID>

Example:

	>pmctl status login session 1000




## Group Details Using `pmctl` tool ##

You can get the group details using commands in `pmctl` tools. The following section lists the commands you can use in the `pmctl` tool to get various group details.


#### Get all Group Details ####

To fetch all the group details, use the following command in the the `pmctl` tool.


	>pmctl status group
	             Gid: 0
	            Name: root
	
	             Gid: 1
	            Name: daemon

	             Gid: 2
	            Name: bin
	
	             Gid: 3
	            Name: sys
	
	             Gid: 4
	            Name: adm
			    .
	            .
	            .
	             Gid: 1001
	            Name: photon-mgmt


#### Get specific Group Details

To fetch specific group details, use the following commands in the `pmctl` tool:

	pmctl status group <GroupName>
or

	pmctl status group <GroupName>

Example:

	>pmctl status group photon-mgmt
	             Gid: 1001
	            Name: photon-mgmt


#### Add a new Group

To add a new group, use the following command in the `pmctl` tool:

	pmctl group add <GroupName> <Gid>
or

	pmctl group add <GroupName>

#### Remove a Group

To remove a group, us the followong command in the `omctl` tool:

	pmctl group remove <GroupName> <Gid>

or


	pmctl group remove <GroupName>


## Group Details Using cURL command ##

The following section list the cURL commands that you can use to fetch the groups details. 

#### Get all Group information

To fetch the group details, execute a GET request in the following format:

	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request GET http://localhost/api/v1/system/group/view

#### Get particuller Group information.

To fetch a specific group details, execute a GET request in the following format:

	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request GET http://localhost/api/v1/system/group/view/<GroupName>



## User Details Using `pmctl` Tool ##

You can use the `pmctl` tool to get the user details. The following section lists the commands to get the user details.



#### Get all User Details

To get all the user details, use the following command in the `pmctl` tool:




	>pmctl status user
	          User Name: root
	                Uid: 0
	                Gid: 0
	              GECOS: root
	     Home Directory: /root

	          User Name: daemon
	                Uid: 1
	                Gid: 1
	              GECOS: daemon
	     Home Directory: /usr/sbin

	          User Name: bin
	                Uid: 2
	                Gid: 2
	              GECOS: bin
	     Home Directory: /bin
	
	          User Name: sys
	                Uid: 3
	                Gid: 3
	              GECOS: sys
	     Home Directory: /dev
	
	          User Name: photon-mgmt
	                Uid: 1001
	                Gid: 1001
	     Home Directory: /home/photon-mgmt



#### Add a New User

To add a new user, use the following command in the `pmctl` tool:


	pmctl user add <UserName> home-dir <HomeDir> groups <groupsList> uid <Uid> gid <Gid> shell <Shell> password <xxxxxxx>
or

	pmctl user a <UserName> -d <HomeDir> -grp <groupsList> -u <Uid> -g <Gid> -s <Shell> -p <xxxxxxx>

#### Remove a User

To remove a user, use the following command in the `pmctl` tool: 

	pmctl user remove <UserName>

or

	pmctl user r <UserName>


## GET User Details ##

To fetch user details, execute a GET request in the following format:

	curl --unix-socket /run/photon-mgmt/photon-mgmt.sock --request GET http://localhost/api/v1/system/user/view