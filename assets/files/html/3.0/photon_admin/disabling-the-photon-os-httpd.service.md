# Disabling the Photon OS httpd.service 

If your application or appliance includes its own HTTP server, you must turn off and disable the HTTP server that comes with Photon OS so that it does not conflict with your own HTTP server. 

To stop it and disable it, run the following commands as root: 

	
```
systemctl stop httpd.service
systemctl disable httpd.service
```
