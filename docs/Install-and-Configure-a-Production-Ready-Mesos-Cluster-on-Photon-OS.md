# Install and Configure a Production Ready Mesos Cluster on Photon OS

## Overview

For this setup I will use 3 Mesos masters and 3 slaves. On each Mesos master I will run a Zookeeper, meaning that we will have 3 Zookeepers as well. The Mesos cluster will be configured with a quorum of 2. For networking Mesos use Mesos-DNS. I tried to run Mesos-DNS as container, but got into some resolving issues, so in my next How-To I will explain how to configure Mesos-DNS and run it through Marathon. Photon hosts will be used for masters and slaves.

**Masters:**

| Hostname | IP Address|
|-
| pt-mesos-master1.example.com | 192.168.0.1 |
| pt-mesos-master2.example.com | 192.168.0.2 |
| pt-mesos-master3.example.com | 192.168.0.3 |

**Agents:**

| Hostname | IP Address|
|-
| pt-mesos-node1.example.com | 192.168.0.4 |
| pt-mesos-node2.example.com | 192.168.0.5 |
| pt-mesos-node3.example.com | 192.168.0.6

## Masters Installation and Configuration 

First of all we will install Zookeeper. Since currently there is a bug in Photon related to the Zookeeper installation I will use the tarball. Do the following for each master:

```
root@pt-mesos-master1 [ ~ ]# mkdir -p /opt/mesosphere && cd /opt/mesosphere && wget http://apache.mivzakim.net/zookeeper/stable/zookeeper-3.4.7.tar.gz
root@pt-mesos-master1 [ /opt/mesosphere ]# tar -xf zookeeper-3.4.7.tar.gz && mv zookeeper-3.4.7 zookeeper
root@pt-mesos-master1 [ ~ ]# cat /opt/mesosphere/zookeeper/conf/zoo.cfg | grep -v '#'
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/var/lib/zookeeper
clientPort=2181
server.1=192.168.0.1:2888:3888
server.2=192.168.0.2:2888:3888
server.3=192.168.0.3:2888:3888
```

Example of Zookeeper systemd configuration file:
```
root@pt-mesos-master1 [ ~ ]# cat /etc/systemd/system/zookeeper.service
[Unit]
Description=Apache ZooKeeper
After=network.target
 
[Service]
Environment="JAVA_HOME=/opt/OpenJDK-1.8.0.51-bin"
WorkingDirectory=/opt/mesosphere/zookeeper
ExecStart=/bin/bash -c "/opt/mesosphere/zookeeper/bin/zkServer.sh start-foreground"
Restart=on-failure
RestartSec=20
User=root
Group=root
 
[Install]
WantedBy=multi-user.target
```

Add server id to the configuration file, so zookeeper will understand the id of your master server. 
This should be done for each master with its own id.

```
root@pt-mesos-master1 [ ~ ]# echo 1 > /var/lib/zookeeper/myid
root@pt-mesos-master1 [ ~ ]# cat /var/lib/zookeeper/myid
1
```

Now lets install the Mesos masters. Do the following for each master:
```
root@pt-mesos-master1 [ ~ ]# yum -y install mesos
Setting up Install Process
Package mesos-0.23.0-2.ph1tp2.x86_64 already installed and latest version
Nothing to do
root@pt-mesos-master1 [ ~ ]# cat /etc/systemd/system/mesos-master.service
[Unit]
Description=Mesos Slave
After=network.target
Wants=network.target
 
[Service]
ExecStart=/bin/bash -c "/usr/sbin/mesos-master \
    --ip=192.168.0.1 \
    --work_dir=/var/lib/mesos \
    --log_dir=/var/log/mesos \
    --cluster=EXAMPLE \
    --zk=zk://192.168.0.1:2181,192.168.0.2:2181,192.168.0.3:2181/mesos \
    --quorum=2"
KillMode=process
Restart=always
RestartSec=20
LimitNOFILE=16384
CPUAccounting=true
MemoryAccounting=true
 
[Install]
WantedBy=multi-user.target
```

Make sure you replace *ip* setting on each master. So far we have 3 masters with a Zookeeper and Mesos packages installed. Let's start zookeeper and mesos-master services on each master:

```
root@pt-mesos-master1 [ ~ ]# systemctl start zookeeper
root@pt-mesos-master1 [ ~ ]# systemctl start mesos-master
root@pt-mesos-master1 [ ~ ]# ps -ef | grep mesos
root     11543     1  7 12:09 ?        00:00:01 /opt/OpenJDK-1.8.0.51-bin/bin/java -Dzookeeper.log.dir=. -Dzookeeper.root.logger=INFO,CONSOLE -cp /opt/mesosphere/zookeeper/bin/../build/classes:/opt/mesosphere/zookeeper/bin/../build/lib/*.jar:/opt/mesosphere/zookeeper/bin/../lib/slf4j-log4j12-1.6.1.jar:/opt/mesosphere/zookeeper/bin/../lib/slf4j-api-1.6.1.jar:/opt/mesosphere/zookeeper/bin/../lib/netty-3.7.0.Final.jar:/opt/mesosphere/zookeeper/bin/../lib/log4j-1.2.16.jar:/opt/mesosphere/zookeeper/bin/../lib/jline-0.9.94.jar:/opt/mesosphere/zookeeper/bin/../zookeeper-3.4.7.jar:/opt/mesosphere/zookeeper/bin/../src/java/lib/*.jar:/opt/mesosphere/zookeeper/bin/../conf: -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.local.only=false org.apache.zookeeper.server.quorum.QuorumPeerMain /opt/mesosphere/zookeeper/bin/../conf/zoo.cfg
root     11581     1  0 12:09 ?        00:00:00 /usr/sbin/mesos-master --ip=192.168.0.1 --work_dir=/var/lib/mesos --log_dir=/var/lob/mesos --cluster=EXAMPLE --zk=zk://192.168.0.2:2181,192.168.0.1:2181,192.168.0.3:2181/mesos --quorum=2
root     11601  9117  0 12:09 pts/0    00:00:00 grep --color=auto mesos
```

## Slaves Installation and Configuration 

The steps for configuring a Mesos slave are very simple and not very different from master installation. The difference is that we won't install zookeeper on each slave. We will also start the Mesos slaves in slave mode and will tell the daemon to join the Mesos masters. Do the following for each slave:

```
root@pt-mesos-node1 [ ~ ]# cat /etc/systemd/system/mesos-slave.service
[Unit]
Description=Photon instance running as a Mesos slave
After=network-online.target,docker.service
  
[Service]
Restart=on-failure
RestartSec=10
TimeoutStartSec=0
ExecStartPre=/usr/bin/rm -f /tmp/mesos/meta/slaves/latest
ExecStart=/bin/bash -c "/usr/sbin/mesos-slave \
    --master=zk://192.168.0.1:2181,192.168.0.2:2181,192.168.0.3:2181/mesos \
        --hostname=$(/usr/bin/hostname) \
        --log_dir=/var/log/mesos_slave \
        --containerizers=docker,mesos \
        --docker=$(which docker) \
        --executor_registration_timeout=5mins \
        --ip=192.168.0.4"
  
[Install]
WantedBy=multi-user.target
```

Please make sure to replace the NIC name under *ip* setting. Start the mesos-slave service on each node.

Now you should have ready Mesos cluster with 3 masters, 3 Zookeepers and 3 slaves. 

If you want to use private docker registry, you will need to edit docker systemd file. 

In my example I am using cse-artifactory.eng.vmware.com registry:

```
root@pt-mesos-node1 [ ~ ]# cat /lib/systemd/system/docker.service
[Unit]
Description=Docker Daemon
Wants=network-online.target
After=network-online.target
  
[Service]
EnvironmentFile=-/etc/sysconfig/docker
ExecStart=/bin/docker -d $OPTIONS -s overlay
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=always
MountFlags=slave
LimitNOFILE=1048576
LimitNPROC=1048576
LimitCORE=infinity
  
[Install]
WantedBy=multi-user.target
  
root@pt-mesos-node1 [ ~ ]# cat /etc/sysconfig/docker
OPTIONS='--insecure-registry cse-artifactory.eng.vmware.com'
root@pt-mesos-node1 [ ~ ]# systemctl daemon-reload && systemctl restart docker
root@pt-mesos-node1 [ ~ ]# ps -ef | grep cse-artifactory
root      5286     1  0 08:39 ?        00:00:00 /bin/docker -d --insecure-registry <your_privet_registry> -s overlay
```

