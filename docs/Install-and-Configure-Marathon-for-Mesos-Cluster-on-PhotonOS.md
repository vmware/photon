# Install and Configure Marathon for Mesos Cluster on PhotonOS

In this How-To I am going to explain how to install and configure Marathon for Mesos cluster. All the following steps should be done on each Mesos master.

First, download Marathon:

```
root@pt-mesos-master2 [ ~ ]# mkdir -p  /opt/mesosphere/marathon/ && cd /opt/mesosphere/marathon/
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]#  curl -O http://downloads.mesosphere.com/marathon/v0.13.0/marathon-0.13.0.tgz
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]# tar -xf marathon-0.13.0.tgz
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]# mv marathon-0.13.0 marathon
```

Create a configuration for Marathon:

```
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]# ls -l /etc/marathon/conf/
total 8
-rw-r--r-- 1 root root 68 Dec 24 14:33 master
-rw-r--r-- 1 root root 71 Dec 24 14:33 zk
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]# cat /etc/marathon/conf/*
zk://192.168.0.2:2181,192.168.0.1:2181,192.168.0.3:2181/mesos
zk://192.168.0.2:2181,192.168.0.1:2181,192.168.0.3:2181/marathon
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]# cat /etc/systemd/system/marathon.service
[Unit]
Description=Marathon
After=network.target
Wants=network.target
 
[Service]
Environment="JAVA_HOME=/opt/OpenJDK-1.8.0.51-bin"
ExecStart=/opt/mesosphere/marathon/bin/start \
    --master zk://192.168.0.2:2181,192.168.0.1:2181,192.168.0.3:2181/mesos \
    --zk zk://192.168.0.2:2181,192.168.0.1:2181,192.168.0.3:2181/marathon
Restart=always
RestartSec=20
 
[Install]
WantedBy=multi-user.target
```

Finally, we need to change the Marathon startup script, since PhotonOS do not use the standard JRE. 

Make sure you add JAVA_HOME to Java path:

```
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]# tail -n3 /opt/mesosphere/marathon/bin/start
# Start Marathon
marathon_jar=$(find "$FRAMEWORK_HOME"/target -name 'marathon-assembly-*.jar' | sort | tail -1)
exec "${JAVA_HOME}/bin/java" "${java_args[@]}" -jar "$marathon_jar" "${app_args[@]}"
```

Now we can start the Marthon service:
```
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]# systemctl start marathon
root@pt-mesos-master2 [ /opt/mesosphere/marathon ]# ps -ef | grep marathon
root     15821     1 99 17:14 ?        00:00:08 /opt/OpenJDK-1.8.0.51-bin/bin/java -jar /opt/mesosphere/marathon/bin/../target/scala-2.11/marathon-assembly-0.13.0.jar --master zk://192.168.0.2:2181,192.168.0.1:2181,192.168.0.3:2181/mesos --zk zk://192.168.0.2:2181,192.168.0.1:2181,192.168.0.3:2181/marathon
root     15854 14692  0 17:14 pts/0    00:00:00 grep --color=auto marathon
```