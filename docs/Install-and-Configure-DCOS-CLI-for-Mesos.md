# Install and Configure DCOS CLI for Mesos

To install the DCOS CLI:
Install virtualenv. The Python tool virtualenv is used to manage the DCOS CLI’s environment.
<source lang="bash" enclose="div">
sudo pip install virtualenv
</source><br />
Tip: On some older Python versions, ignore any ‘Insecure Platform’ warnings. For more information, see https://virtualenv.pypa.io/en/latest/installation.html.
From the command line, create a new directory named dcos and navigate into it.
<source lang="bash" enclose="div">
$ mkdir dcos
$ cd dcos
$ curl -O https://downloads.mesosphere.io/dcos-cli/install.sh
</source><br />
Run the DCOS CLI install script, where &lt;hosturl&gt; is the hostname of your master node prefixed with http://:
<source lang="bash" enclose="div">
$ bash install.sh <install_dir> <mesos-master-host>
</source><br />
For example, if the hostname of your Mesos master node is mesos-master.example.com:
<source lang="bash" enclose="div">
$ bash install.sh . http://mesos-master.example.com
</source><br />
Follow the on-screen DCOS CLI instructions and enter the Mesosphere verification code. You can ignore any Python ‘Insecure Platform’ warnings.
<source lang="bash" enclose="div">
Confirm whether you want to add DCOS to your system PATH:
$ Modify your bash profile to add DCOS to your PATH? [yes/no]
</source><br />
Since DCOS CLI is used for DCOS cluster, reconfigure Marathon and Mesos masters URLs with the following commands:
<source lang="bash" enclose="div">
dcos config set core.mesos_master_url http://<mesos-master-host>:5050
dcos config set marathon.url http://<marathon-host>:8080
</source><br />
<br /><br />
Next - [[Install and Configure Mesos DNS on a Mesos Cluster]]