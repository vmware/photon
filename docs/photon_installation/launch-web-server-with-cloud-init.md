# Launch the Web Server with Cloud-Init

To eliminate the manual effort of running Docker, you can add `docker run` and its arguments to the cloud-init user data file by using `runcmd`: 

	#cloud-config
	hostname: photon-on-01
	groups:
	- cloud-admins
	- cloud-users
	users:
	- default
	- name: photonadmin
	   gecos: photon test admin user
	   primary-group: cloud-admins
	   groups: cloud-users
	   lock-passwd: false
	   passwd: vmware
	- name: photonuser
	   gecos: photon test user
	   primary-group: cloud-users
	   groups: users
	   passwd: vmware
	packages:
	- vim
	runcmd:
	- docker run -p 80:80 vmwarecna/nginx

To try this addition, run another instance with the new cloud-init data source and then get the public IP address of the instance to check that the Nginx web server is running. 