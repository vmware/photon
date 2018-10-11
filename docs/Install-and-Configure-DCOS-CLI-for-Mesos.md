# Install and Configure DCOS CLI for Mesos

To install the DCOS CLI:
Install virtualenv. The Python tool virtualenv is used to manage the DCOS CLI’s environment.

```
sudo pip install virtualenv
```

Tip: On some older Python versions, ignore any ‘Insecure Platform’ warnings. For more information, see https://virtualenv.pypa.io/en/latest/installation.html. From the command line, create a new directory named dcos and navigate into it.

```
$ mkdir dcos
$ cd dcos
$ curl -O https://downloads.mesosphere.io/dcos-cli/install.sh
```

Run the DCOS CLI install script, where <hosturl> is the hostname of your master node prefixed with http://:
```
$ bash install.sh <install_dir> <mesos-master-host>
```

For example, if the hostname of your Mesos master node is mesos-master.example.com:

```
$ bash install.sh . http://mesos-master.example.com
```

Follow the on-screen DCOS CLI instructions and enter the Mesosphere verification code. You can ignore any Python ‘Insecure Platform’ warnings.

```
Confirm whether you want to add DCOS to your system PATH:
$ Modify your bash profile to add DCOS to your PATH? [yes/no]
```

Since DCOS CLI is used for DCOS cluster, reconfigure Marathon and Mesos masters URLs with the following commands:

```
dcos config set core.mesos_master_url http://<mesos-master-host>:5050
dcos config set marathon.url http://<marathon-host>:8080
```
