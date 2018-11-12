# Creating a Stand-Alone Photon Machine with cloud-init

Cloud-init can customize a Photon OS virtual machine by using the `nocloud` data source. The nocloud data source bundles the cloud-init metadata and user data into a ISO that acts as a seed when you boot the machine. This seed.iso delivers the metadata and the user data without requiring a network connection. 

Here's how customize a Photon OS VM with a nocloud data source:

First, create the metadata file with the following lines in the [YAML](http://www.yaml.org/start.html) format and name it `meta-data`:

	instance-id: iid-local01
	local-hostname: cloudimg

Second, create the user data file with the following lines in YAML and name it user-data:

	#cloud-config
	hostname: testhost
	packages:
	 - vim

Third, generate the ISO that will serve as the seed; the ISO must have the volume ID set to `cidata`. In this example, the ISO is generated on an Ubuntu 14.04 computer containing the files named `meta-data` and `user-data` in the local directory: 

	genisoimage -output seed.iso -volid cidata -joliet -rock user-data meta-data

The ISO now appears in the current directory: 

	steve@ubuntu:~$ ls
	meta-data seed.iso user-data

Optionally, you can check the ISO that you generated on Ubuntu by transferring the ISO to the root directory of your Photon OS machine and then running the following command: 

	cloud-init --file seed.iso --debug init

After running the cloud-init command above, check the cloud-init log file: 

	more /var/log/cloud-init.log

Finally, attach the ISO to the Photon OS virtual machine as a CD-ROM and reboot it so that the changes specified by seed.iso take effect. In this case, cloud-init sets the hostname and adds the vim package.