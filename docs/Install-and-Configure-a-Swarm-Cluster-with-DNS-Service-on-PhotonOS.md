<sub>Posted on January 13, 2016 by [https://il.linkedin.com/in/tgabay '''Tal Gabay''']</sub>

= Overview =

In this How-To, the steps for installing and configuring a Docker Swarm cluster, alongside DNS and Zookeeper, will be presented.
The cluster that will be set up will be on VMware Photon hosts. <br />
<br />
A prerequisite to using this guide is to be familiar with Docker Swarm - information can be found [https://docs.docker.com/swarm/ here].

== Cluster description ==

The cluster will have 2 Swarm Managers and 3 Swarm Agents:

=== Masters ===

{| class="wikitable"
! style="text-align: center; font-weight: bold;" | Hostname
! style="font-weight: bold;" | IP Address
|-
| pt-swarm-master1.example.com
| 192.168.0.1
|-
| pt-swarm-master2.example.com
| 192.168.0.2
|}

=== Agents ===

{| class="wikitable"
! style="text-align: center; font-weight: bold; font-size: 0.100em;" | Hostname
! style="font-weight: bold;" | IP Address
|-
| pt-swarm-agent1.example.com
| 192.168.0.3
|-
| pt-swarm-agent2.example.com
| 192.168.0.4
|-
| pt-swarm-agent3.example.com
| 192.168.0.5
|}<br />

= Docker Swarm Installation and Configuration =

== Setting Up the Managers ==

The following steps should be done on both managers.<br />
Docker Swarm supports multiple methods of using service discovery, but in order to use failover, Consul, etcd or Zookeeper must be used. In this guide, Zookeeper will be used.<br />
Download the latest stable version of Zookeeper and create the '' zoo.cfg '' file under the '' conf '' directory:
<br />
<br />

=== Zookeeper installation ===

<source lang="bash" enclose="div">
root@pt-swarm-master1 [ ~ ]# mkdir -p /opt/swarm && cd /opt/swarm && wget http://apache.mivzakim.net/zookeeper/stable/zookeeper-3.4.6.tar.gz
root@pt-swarm-master1 [ /opt/swarm ]# tar -xf zookeeper-3.4.6.tar.gz && mv zookeeper-3.4.6 zookeeper
root@pt-swarm-master1 [ ~ ]# cat /opt/swarm/zookeeper/conf/zoo.cfg | grep -v '#'
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/var/lib/zookeeper
clientPort=2181
server.1=192.168.0.1:2888:3888
server.2=192.168.0.2:2888:3888
</source><br />
The dataDir should be an empty, existing directory.
From the Zookeeper documentation: Every machine that is part of the ZooKeeper ensemble should know about every other machine in the ensemble. You accomplish this with the series of lines of the form server.id=host:port:port. You attribute the server id to each machine by creating a file named myid, one for each server, which resides in that server's data directory, as specified by the configuration file parameter dataDir. The myid file consists of a single line containing only the text of that machine's id. So myid of server 1 would contain the text "1" and nothing else. The id must be unique within the ensemble and should have a value between 1 and 255.
<br />
<br />
Set Zookeeper ID
<source lang="bash" enclose="div">
root@pt-swarm-master1 [ ~ ]# echo 1 > /var/lib/zookeeper/myid
</source><br />
Project Photon uses [https://en.wikipedia.org/wiki/Systemd Systemd] for services, so a zookeeper service should be created using systemd unit file.<br />
<source lang="bash" enclose="div">
root@pt-swarm-master1 [ ~ ]# cat /etc/systemd/system/zookeeper.service
[Unit]
Description=Apache ZooKeeper
After=network.target
 
[Service]
Environment="JAVA_HOME=/opt/OpenJDK-1.8.0.51-bin"
WorkingDirectory=/opt/swarm/zookeeper
ExecStart=/bin/bash -c "/opt/swarm/zookeeper/bin/zkServer.sh start-foreground"
Restart=on-failure
RestartSec=20
User=root
Group=root
 
[Install]
WantedBy=multi-user.target
</source><br />
Zookeeper comes with OpenJDK, so having Java on the Photon host is not a prerequisite. Simply direct the Environment variable to the location where the Zookeeper was extracted.
Now you need to enable and start the service. Enabling the service will make sure that if the host restarts for some reason, the service will automatically start.<br />
<source lang="bash" enclose="div">
root@pt-swarm-master1 [ ~ ]# systemctl enable zookeeper
root@pt-swarm-master1 [ ~ ]# systemctl start zookeeper
</source><br />
Verify that the service was able to start:<br />
<source lang="bash" enclose="div">
root@pt-swarm-master1 [ ~ ]# systemctl status zookeeper
zookeeper.service - Apache ZooKeeper
   Loaded: loaded (/etc/systemd/system/zookeeper.service; enabled)
   Active: active (running) since Tue 2016-01-12 00:27:45 UTC; 10s ago
 Main PID: 4310 (java)
   CGroup: /system.slice/zookeeper.service
           `-4310 /opt/OpenJDK-1.8.0.51-bin/bin/java -Dzookeeper.log.dir=. -Dzookeeper.root.logger=INFO,CONSOLE -cp /opt/swarm/zookeeper/bin/../build/classes:/opt/swarm/zookeeper/bin/../build/lib/*.jar:/opt/s...
</source><br />
On the Manager you elected to be the Swarm Leader (primary), execute the following (if you do not have a specific leader in mind, choose one of the managers randomly):
<source lang="bash" enclose="div">
root@pt-swarm-master1 [ ~ ]# docker run -d --name=manager1 -p 8888:2375 swarm manage --replication --advertise 192.168.0.1:8888 zk://192.168.0.1,192.168.0.2/swarm
</source>
* '' docker run -d ''- run the container in the background.
* '' --name=manager1 ''- give the container a name instead of the auto-generated one.
* '' -p 8888:2375 ''- publish a container's port(s) to the host. In this case, when you connect to the host in port 8888, it connects to the container in port 2375.
* swarm - the image to use for the container.
* manage - the command to send to the container once it's up, alongside the rest of the parameters.
* '' --replication '' - tells swarm that the manager is part of a a multi-manager configuration and that this primary manager competes with other manager instances for the primary role. The primary manager has the authority to manage the cluster, replicate logs, and replicate events that are happening inside the cluster.
* '' --advertise 192.168.0.1:8888 ''- specifies the primary manager address. Swarm uses this address to advertise to the cluster when the node is elected as the primary.
* '' zk://192.168.0.1,192.168.0.2/swarm ''- specifies the Zookeepers' location to enable service discovery. The /swarm path is arbitrary, just make sure that every node that joins the cluster specifies that same path (it is meant to enable support for multiple clusters with the same Zookeepers).<br />
<br />
On the second manager, execute the following:
<source lang="bash" enclose="div">
root@pt-swarm-master2 [ ~ ]# docker run -d --name=manager2 -p 8888:2375 swarm manage --replication --advertise 192.168.0.2:8888 zk://192.168.0.1,192.168.0.2/swarm
</source>
Notice that the only difference is the --advertise flag value. The first manager will not lose leadership following this command.<br />
<br />
Now 2 managers are alive, one is the primary and another is the replica. When we now look at the docker info on our primary manager, we can see the following information:
<source lang="bash" enclose="div">
docker-client:~$ docker -H tcp://192.168.0.1:8888 info
Containers: 0
Images: 0
Role: primary
Strategy: spread
Filters: health, port, dependency, affinity, constraint
Nodes: 0
CPUs: 0
Total Memory: 0 B
Name: 82b8516efb7c
</source>
There are a few things that are worth noticing:
* The info command can be executed from ANY machine that can reach the master. The -H tcp://&lt;ip&gt;:&lt;port&gt; command specifies that the docker command should be executed on a remote host.
* Containers - this is the result of the docker ps -a command for the cluster we just set up.
* Images - the result of the docker images command.
* Role - as expected, this is the primary manager.
* Strategy - Swarm has a number of strategies it supports for setting up containers in the cluster. spread means that a new container will run on the node with the least amount of containers on it.
* Filters - Swarm can choose where to run containers based on different filters supplied in the command line. More info can be found [https://docs.docker.com/swarm/scheduler/filter/ here].<br />
<br />
When we now look at the docker info on our replicated manager, we can see the following information:
<source lang="bash" enclose="div">
docker-client:~$ docker -H tcp://192.168.0.2:8888 info
Containers: 0
Images: 0
Role: replica
Primary: 192.168.0.1:8888
Strategy: spread
Filters: health, port, dependency, affinity, constraint
Nodes: 0
CPUs: 0
Total Memory: 0 B
Name: ac06f826e507
</source>
Notice that the only differences between both managers are:
Role: as expected, this is the replicated manager.
Primary: contains the primary manager.<br />
<br />

== Setting Up the Agents ==

In Swarm, in order for a node to become a part of the cluster, it should "join" that said cluster - do the following for each of the agents.
Edit the '' /usr/lib/systemd/system/docker.service '' file so that each agent will be able to join the cluster:
<source lang="bash" enclose="div">
root@pt-swarm-agent1 [ ~ ]# cat /usr/lib/systemd/system/docker.service
[Unit]
Description=Docker Daemon
Wants=network-online.target
After=network-online.target
 
[Service]
ExecStart=/bin/docker daemon -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-advertise eno16777984:2375 --cluster-store zk://192.168.0.1,192.168.0.2/swarm
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=always
MountFlags=slave
LimitNOFILE=1048576
LimitNPROC=1048576
LimitCORE=infinity
 
[Install]
WantedBy=multi-user.target
</source>
* '' -H tcp://0.0.0.0:2375 ''- This ensures that the Docker remote API on Swarm Agents is available over TCP for the Swarm Manager.
* '' -H unix:///var/run/docker.sock ''- The Docker daemon can listen for Docker Remote API requests via three different types of Socket: unix, tcp, and fd. 
** tcp - If you need to access the Docker daemon remotely, you need to enable the tcp Socket.
** fd - On Systemd based systems, you can communicate with the daemon via Systemd socket activation.
* '' --cluster-advertise <NIC>:2375 ''- advertises the machine on the network by stating the ethernet card and the port used by the Swarm Managers.
* '' --cluster-store zk://192.168.0.1,192.168.0.2/swarm ''- as we defined before, the service discovery being used here is Zookeeper.
<br />
Enable and start the docker service:
<source lang="bash" enclose="div">
root@pt-swarm-agent1 [ ~ ]# systemctl enable docker
root@pt-swarm-agent1 [ ~ ]# systemctl daemon-reload && systemctl restart docker
root@pt-swarm-agent1 [ ~ ]# systemctl status docker
docker.service - Docker Daemon
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled)
   Active: active (running) since Tue 2016-01-12 00:46:18 UTC; 4s ago
 Main PID: 11979 (docker)
   CGroup: /system.slice/docker.service
           `-11979 /bin/docker daemon -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-advertise eno16777984:2375 --cluster-store zk://192.168.0.1,192.168.0.2/swarm
</source><br />
All that remains is to have the agents join the cluster:
<source lang="bash" enclose="div">
root@pt-swarm-agent1 [ ~ ]# docker run -d swarm join --advertise=192.168.0.3:2375 zk://192.168.0.1,192.168.0.2/swarm
</source><br />
A look at the output of the docker info command will now show:
<source lang="bash" enclose="div">
docker-client:~$ docker -H tcp://192.168.0.1:8888 info
Containers: 3
Images: 9
Role: primary
Strategy: spread
Filters: health, port, dependency, affinity, constraint
Nodes: 3
 pt-swarm-agent1.example.com: 192.168.0.3:2375
  └ Status: Healthy
  └ Containers: 1
  └ Reserved CPUs: 0 / 1
  └ Reserved Memory: 0 B / 2.055 GiB
  └ Labels: executiondriver=native-0.2, kernelversion=4.1.3-esx, operatingsystem=VMware Photon/Linux, storagedriver=overlay
 pt-swarm-agent2.example.com: 192.168.0.4:2375
  └ Status: Healthy
  └ Containers: 1
  └ Reserved CPUs: 0 / 1
  └ Reserved Memory: 0 B / 2.055 GiB
  └ Labels: executiondriver=native-0.2, kernelversion=4.1.3-esx, operatingsystem=VMware Photon/Linux, storagedriver=overlay
 pt-swarm-agent3.example.com: 192.168.0.5:2375
  └ Status: Healthy
  └ Containers: 1
  └ Reserved CPUs: 0 / 1
  └ Reserved Memory: 0 B / 2.055 GiB
  └ Labels: executiondriver=native-0.2, kernelversion=4.1.3-esx, operatingsystem=VMware Photon/Linux, storagedriver=overlay
CPUs: 3
Total Memory: 6.166 GiB
Name: 82b8516efb7c
</source>

== Setting Up DNS ==

Docker does not have its own self-provided DNS so we use a [https://github.com/ahmetalpbalkan/wagl wagl] DNS.
Setting it up is very simple. In this case, one of the masters will also be the DNS. Simply execute:
<source lang="bash" enclose="div">
docker-client:~$ docker run -d --restart=always --name=dns -p 53:53/udp --link manager1:swarm ahmet/wagl wagl --swarm tcp://swarm:2375
</source>
* '' --restart=always ''- Always restart the container regardless of the exit status. When you specify always, the Docker daemon will try to restart the container continuously. The container will also always start on daemon startup, regardless of the current state of the container.
* '' --link manager1:swarm ''- link the manager1 container (by name) and give it the alias swarm.
That's it, DNS is up and running.

= Test Your Cluster =

== Running Nginx ==

Execute the following commands from any docker client:
<source lang="bash" enclose="div">
docker-client:~$ docker -H tcp://192.168.0.1:8888 run -d -l dns.service=api -l dns.domain=example -p 80:80 vmwarecna/nginx
docker-client:~$ docker -H tcp://192.168.0.1:8888 run -d -l dns.service=api -l dns.domain=example -p 80:80 vmwarecna/nginx
</source>
Note that this is the same command, executed twice. It tells the master to run 2 of the similar containers, each of which has 2 dns labels.<br />
Now, from any container in the cluster that has dnsutils, you can execute the following (for example):
<source lang="bash" enclose="div">
root@13271a2d0fcb:/# dig +short A api.example.swarm
192.168.0.3
192.168.0.4
root@13271a2d0fcb:/# dig +short SRV _api._tcp.example.swarm
1 1 80 192.168.0.3.
1 1 80 192.168.0.4.
</source>