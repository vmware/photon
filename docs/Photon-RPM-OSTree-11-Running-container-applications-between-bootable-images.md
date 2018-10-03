In this chapter, we want to test a docker application and make sure that all the settings and downloads done in one bootable filetree are going to be saved into writable folders and be available in the other image, in other words after reboot from the other image, everything is available exactly the same way.   
We are going to do this twice: first, to verify an existing bootable image installed in parallel and then create a new one.

### 11.1 Downloading a docker container appliance
Photon OS comes with docker package installed and configured, but we expect that the docker daemon is inactive (not started). Configuration file /usr/lib/systemd/system/docker.service is read-only (remember /usr is bound as read-only). 
```
root@sample-host-def [ ~ ]# systemctl status docker
* docker.service - Docker Daemon
   Loaded: loaded (/usr/lib/systemd/system/docker.service; disabled)
   Active: inactive (dead)

root@sample-host-def [ ~ ]# cat /usr/lib/systemd/system/docker.service
[Unit]
Description=Docker Daemon
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/bin/docker -d -s overlay
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=always
MountFlags=slave
LimitNOFILE=1048576
LimitNPROC=1048576
LimitCORE=infinity

[Install]
WantedBy=multi-user.target
```
Now let's enable docker daemon to start at boot time - this will create a symbolic link into writable folder /etc/systemd/system/multi-user.target.wants to its systemd configuration, as with all other systemd controlled services. 
```
root@sample-host-def [ ~ ]# systemctl enable docker
Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /usr/lib/systemd/system/docker.service.

root@sample-host-def [ ~ ]# ls -l /etc/systemd/system/multi-user.target.wants
total 0
lrwxrwxrwx 1 root root 38 Sep  6 08:38 docker.service -> /usr/lib/systemd/system/docker.service
lrwxrwxrwx 1 root root 47 Aug 28 20:21 iptables.service -> ../../../../lib/systemd/system/iptables.service
lrwxrwxrwx 1 root root 47 Aug 28 20:21 remote-fs.target -> ../../../../lib/systemd/system/remote-fs.target
lrwxrwxrwx 1 root root 50 Aug 28 20:21 sshd-keygen.service -> ../../../../lib/systemd/system/sshd-keygen.service
lrwxrwxrwx 1 root root 43 Aug 28 20:21 sshd.service -> ../../../../lib/systemd/system/sshd.service
lrwxrwxrwx 1 root root 55 Aug 28 20:21 systemd-networkd.service -> ../../../../lib/systemd/system/systemd-networkd.service
lrwxrwxrwx 1 root root 55 Aug 28 20:21 systemd-resolved.service -> ../../../../lib/systemd/system/systemd-resolved.service
```
To verify that the symbolic link points to a file in a read-only directory, try to make a change in this file using vim and save. you'll get an error: "/usr/lib/systemd/system/docker.service" E166: Can't open linked file for writing".  
Finally, let's start the daemon, check again that is active. 
```
root@sample-host-def [ ~ ]# systemctl start docker

root@sample-host-def [ ~ ]# systemctl status -l docker
* docker.service - Docker Daemon
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled)
   Active: active (running) since Sun 2015-09-06 08:56:30 UTC; 42s ago
 Main PID: 349 (docker)
   CGroup: /system.slice/docker.service
           `-349 /bin/docker -d -s overlay

Sep 06 08:56:30 sample-host-def docker[349]: Warning: '-d' is deprecated, it will be removed soon. See usage.
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30Z" level=warning msg="please use 'docker daemon' instead."
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30.617969465Z" level=info msg="Option DefaultDriver: bridge"
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30.618264109Z" level=info msg="Option DefaultNetwork: bridge"
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30.632397533Z" level=info msg="Listening for HTTP on unix (/var/run/docker.sock)"
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30.637516253Z" level=info msg="Firewalld running: false"
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30.786748372Z" level=info msg="Loading containers: start."
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30.787252697Z" level=info msg="Loading containers: done."
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30.787410576Z" level=info msg="Daemon has completed initialization"
Sep 06 08:56:30 sample-host-def docker[349]: time="2015-09-06T08:56:30.787610148Z" level=info msg="Docker daemon" commit=d12ea79 execdriver=native-0.2 graphdriver=overlay version=1.8.1
```
We'll ask docker to run Ubuntu Linux in a container. Since it's not present locally, it's going to be downloaded first from the official docker repository https://hub.docker.com/_/ubuntu/.
```
root@sample-host-def [ ~ ]# docker ps -a
CONTAINER ID        IMAGE            COMMAND      CREATED           STATUS              PORTS       NAMES

root@sample-host-def [ ~ ]# docker run -it ubuntu
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
d3a1f33e8a5a: Downloading [=========================================>         ] 54.55 MB/65.79 MB
c22013c84729: Download complete 
d74508fb6632: Download complete 
91e54dfb1179: Download complete 
```
When downloading is complete, it comes to Ubuntu root prompt with assigned host name d07ebca78051, that is actually the Container ID. Let's verify it's indeed the expected OS.
```
root@sample-host-def [ ~ ]# docker run -it ubuntu
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
d3a1f33e8a5a: Pull complete 
c22013c84729: Pull complete 
d74508fb6632: Pull complete 
91e54dfb1179: Already exists 
library/ubuntu:latest: The image you are pulling has been verified. Important: image verification is a tech preview feature and should not be relied on to provide security.
Digest: sha256:fde8a8814702c18bb1f39b3bd91a2f82a8e428b1b4e39d1963c5d14418da8fba
Status: Downloaded newer image for ubuntu:latest

root@d07ebca78051:/# cat /etc/os-release
NAME="Ubuntu"
VERSION="14.04.3 LTS, Trusty Tahr"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 14.04.3 LTS"
VERSION_ID="14.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
root@d07ebca78051:/#
```
Now let's write a file into Ubuntu home directory
```
echo "Ubuntu file" > /home/myfile
root@d07ebca78051:/home# cat /home/myfile
Ubuntu file
```
We'll exit back to the Photon prompt and if it's stopped, we will re-start it.
```
root@d07ebca78051:/# exit
exit

root@sample-host-def [ ~ ]# docker ps -a
CONTAINER ID    IMAGE   COMMAND       CREATED         STATUS                      PORTS   NAMES
d07ebca78051    ubuntu  "/bin/bash"   3 minutes ago   Exited (0) 13 seconds ago           kickass_hodgkin

root@photon-host-cus1 [ ~ ]# docker start  d07ebca78051
d07ebca78051

root@photon-host-cus1 [ ~ ]# docker ps -a
CONTAINER ID    IMAGE   COMMAND       CREATED         STATUS                      PORTS   NAMES
d07ebca78051    ubuntu  "/bin/bash"   16 minutes ago  Up 5 seconds                        kickass_hodgkin
```

### 11.2 Rebooting into an existing image
Now let's reboot the machine and select the other image. First, we'll verify that the docker daemon is automaically started.
```
root@photon-host-cus1 [ ~ ]# systemctl status docker
* docker.service - Docker Daemon
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled)
   Active: active (running) since Sun 2015-09-06 11:19:05 UTC; 2min 9s ago
 Main PID: 292 (docker)
   CGroup: /system.slice/docker.service
           `-292 /bin/docker -d -s overlay
   ...
```
Next, is the Ubuntu OS container still there?
```
root@photon-host-cus1 [ ~ ]# docker ps -a 
CONTAINER ID    IMAGE     COMMAND      CREATED          STATUS                     PORTS   NAMES
57dcac5d0490    ubuntu    "/bin/bash"  25 minutes ago   Exited (137) 5 minutes ago         sad_banach
```
It is, so let's start it, attach and verify that our file is persisted, then add another line to it and save, exit.
```
root@photon-host-cus1 [ ~ ]# docker start -i  57dcac5d0490
root@57dcac5d0490:/# cat /home/myfile 
Ubuntu file
root@57dcac5d0490:/# echo "booted into existing image" >> /home/myfile
root@57dcac5d0490:/# exit
```
### 11.3 Reboot into a newly created image
Let's upgrade and replace the .0 image by a .3 build that contains git and also perl_YAML (because it is a dependency of git).
```
root@photon-host-cus1 [ ~ ]# rpm-ostree status
  TIMESTAMP (UTC)         VERSION               ID             OSNAME     REFSPEC                              
* 2015-09-04 00:36:37     1.0_tp2_minimal.2     092e21d292     photon     photon:photon/tp2/x86_64/minimal     
  2015-08-20 22:27:43     1.0_tp2_minimal       2940e10c4d     photon     photon:photon/tp2/x86_64/minimal     

root@photon-host-cus1 [ ~ ]# rpm-ostree upgrade
Updating from: photon:photon/tp2/x86_64/minimal

43 metadata, 209 content objects fetched; 19992 KiB transferred in 0 seconds
Copying /etc changes: 5 modified, 0 removed, 19 added
Transaction complete; bootconfig swap: yes deployment count change: 0
Freed objects: 16.2 MB
Added:
  git-2.1.2-1.ph1tp2.x86_64
  perl-YAML-1.14-1.ph1tp2.noarch
Upgrade prepared for next boot; run "systemctl reboot" to start a reboot

root@photon-host-cus1 [ ~ ]# rpm-ostree status
  TIMESTAMP (UTC)         VERSION               ID             OSNAME     REFSPEC                              
  2015-09-06 18:12:08     1.0_tp2_minimal.3     d16aebd803     photon     photon:photon/tp2/x86_64/minimal     
* 2015-09-04 00:36:37     1.0_tp2_minimal.2     092e21d292     photon     photon:photon/tp2/x86_64/minimal  
```
After reboot from 1.0_tp2_minimal.3 build, let's check that the 3-way /etc merge succeeded as expected. The docker.service slink is still there, and docker demon restarted at boot.
```
root@photon-host-cus1 [ ~ ]# ls -l /etc/systemd/system/multi-user.target.wants/docker.service 
lrwxrwxrwx 1 root root 38 Sep  6 12:50 /etc/systemd/system/multi-user.target.wants/docker.service -> /usr/lib/systemd/system/docker.service

root@photon-host-cus1 [ ~ ]# systemctl status docker
* docker.service - Docker Daemon
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled)
   Active: active (running) since Sun 2015-09-06 12:56:33 UTC; 1min 27s ago
 Main PID: 292 (docker)
   CGroup: /system.slice/docker.service
           `-292 /bin/docker -d -s overlay

   ...   
```  
Let's revisit the Ubuntu container. Is the container still there? is myfile persisted?
```
root@photon-host-cus1 [ ~ ]# docker ps -a
CONTAINER ID   IMAGE       COMMAND      CREATED       STATUS                        PORTS   NAMES
57dcac5d0490   ubuntu      "/bin/bash"  2 hours ago   Exited (0) About an hour ago          sad_banach

root@photon-host-cus1 [ ~ ]# docker start 57dcac5d0490

root@57dcac5d0490:/# cat /home/myfile
Ubuntu file
booted into existing image
root@57dcac5d0490:/# echo "booted into new image" >> /home/myfile
```

[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous page|Photon RPM-OSTree:-10-Remotes]] | [[ Next page >|Photon-RPM-OSTree:-Install-or-rebase-to-Photon-OS-2.0]]