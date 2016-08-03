Overview
=================
```cloud-init``` is a multi-distribution package that handles early initialization of a cloud instance.

In-depth documentation for cloud-init is available here:

[https://cloudinit.readthedocs.org/en/latest/](https://cloudinit.readthedocs.org/en/latest/)

Supported installations
=================

Both the full version of and the minimal version of Photon OS support cloud-init. 

Supported capabilities
=================

Photon OS supports the following cloud-init capabilities:


* run commands: execute a list of commands with output to console.
* configure ssh keys: add an entry to ~/.ssh/authorized_keys for the configured user.
* install package: install additional packages on first boot.
* configure networking: update /etc/hosts, hostname, etc.
* write files: write arbitrary files to disk.
* add yum repository: add a yum repository to /etc/yum.repos.d.
* create groups and users: add groups and users to the system and set properties for them. 
* run yum upgrade: upgrade all packages.
* reboot: reboot or power off when done with cloud-init.


Getting Started
=================
The Amazon Machine Image of Photon OS has an ```ec2 datasource``` turned on by default so an ```ec2``` configuration is accepted.
However, for testing, the following methods provide ways to do ```cloud-init``` with a standalone instance of Photon OS.

Using a Seed ISO
----------------
This will be using the ```nocloud``` data source. In order to initialize the system in this way, an ISO file needs to be created with a meta-data file and an user-data file as shown below:
```
$ { echo instance-id: iid-local01; echo local-hostname: cloudimg; } > meta-data
$ printf "#cloud-config\nhostname: testhost\n" > user-data
$ genisoimage  -output seed.iso -volid cidata -joliet -rock user-data meta-data
```

Attach the `seed.iso` generated above to your machine and reboot for the init to take effect.
In this case, the hostname is set to ```testhost```.

Using a Seed Disk File
----------------
To init using local disk files, do the following:
```
mkdir /var/lib/cloud/seed/nocloud
cd /var/lib/cloud/seed/nocloud
$ { echo instance-id: iid-local01; echo local-hostname: cloudimg; } > meta-data
$ printf "#cloud-config\nhostname: testhost\n" > user-data
```
Reboot the machine and the hostname will be set to `testhost`.

Frequencies
-----------
Cloud-init modules have predetermined frequencies. Based on the frequency setting, multiple runs will yield different results. For the scripts to always run, remove the `instances` directory before rebooting.
```
rm -rf /var/lib/cloud/instances
```

Module Frequency Info
------------------------------------
Name                  |  Frequency
----------------------|-------------
disable_ec2_metadata  | Always
users_groups          | Instance
write_files           | Instance
update_hostname       | Always
final_message         | Always
resolv_conf           | Instance
growpart              | Always
update_etc_hosts      | Always
power_state_change    | Instance
phone_home            | Instance
