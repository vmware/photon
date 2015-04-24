Overview
=================
```cloud-init``` is the defacto multi-distribution package that handles early initialization of a cloud instance.

In-depth documentation for cloud-init is available here: https://cloudinit.readthedocs.org/en/latest/

Supported installations
=================
```Photon Container OS (Minimal)```

```Photon Full OS (All)```

Supported capabilities
=================
```Photon``` supports ```cloud-init``` starting with the following capabilities
<dl>
<dt>```run commands```</dt>
<dd>execute a list of commands with output to console.</dd>
<dt>```configure ssh keys```</dt>
<dd>add entry to ~/.ssh/authorized_keys for the configured user</dd>
<dt>```install package```</dt>
<dd>install additional packages on first boot</dd>
<dt>```configure networking```</dt>
<dd>update /etc/hosts, hostname etc</dd>
<dt>```write files```</dt>
<dd>write arbitrary file(s) to disk</dd>
<dt>```add yum repo```</dt>
<dd>add a yum repository to /etc/yum.repos.d</dd>
<dt>```create groups and users```</dt>
<dd>add groups and users to the system. set user/group properties</dd>
<dt>```run yum upgrade```</dt>
<dd>upgrade all packages</dd>
<dt>```reboot```</dt>
<dd>reboot or power off when done with cloud-init</dd>
</dl>

Getting Started
=================
photon cloud config has ```ec2 datasource``` turned on by default so an ```ec2``` configuration is accepted.
However, for testing, the following methods provide ways to do ```cloud-init``` with ```photon``` standalone.

Using a seed iso
----------------
This will be using the ```nocloud``` datasource. In order to init this way, an iso file needs to be created with a meta-data and an user-data file as shown below
```
$ { echo instance-id: iid-local01; echo local-hostname: cloudimg; } > meta-data
$ printf "#cloud-config\nhostname: testhost\n" > user-data
$ genisoimage  -output seed.iso -volid cidata -joliet -rock user-data meta-data
```

Attach the above generated seed.iso to your machine and reboot for the init to take effect.
In this case, the hostname is set to ```testhost```

Using a seed disk file
----------------
To init using local disk files, do the following
```
mkdir /var/lib/cloud/seed/nocloud
cd /var/lib/cloud/seed/nocloud
$ { echo instance-id: iid-local01; echo local-hostname: cloudimg; } > meta-data
$ printf "#cloud-config\nhostname: testhost\n" > user-data
```
Reboot the machine and the hostname will be set to `testhost`

Frequencies
-----------
cloud-init modules have pre-determined frequencies. Based on the frequency setting, multiple runs will yield different results.
For the scripts to run always, remove instances folder before reboot.
```
rm -rf /var/lib/cloud/instances
```

Module frequency info
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
