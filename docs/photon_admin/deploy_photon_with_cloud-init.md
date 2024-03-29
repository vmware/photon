# Deploy Photon OS With `cloud-init`

You can deploy Photon OS with `cloud-init` in the following ways: 

* As a stand-alone Photon machine
* In Amazon Elastic Compute Cloud, called EC2
* In the Google cloud through the Google Compute Engine, or GCE
* In a VMware Vsphere private cloud 

When a cloud instance of Photon OS starts, `cloud-init` requires a data source. The data source can be an EC2 file for Amazon's cloud platform, a `seed.iso` file for a stand-alone instance of Photon OS, or the internal capabilities of a system for managing virtual machines, such as VMware vSphere or vCenter. Cloud-init also includes data sources for OpenStack, Apache CloudStack, and OVF. The data source comprises two parts: 

1. Metadata
2. User data

The metadata gives the cloud service provider instructions on how to implement the Photon OS machine in the cloud infrastructure. Metadata typically includes the instance ID and the local host name. 

The user data contains the commands and scripts that Photon OS executes when it starts in the cloud. The user data commonly takes the form of a shell script or a YAML file containing a cloud configuration. The [cloud-init overview](https://launchpad.net/cloud-init) and [cloud-init documentation](https://cloudinit.readthedocs.org/en/latest/) contains information about the types of data sources and the formats for metadata and user data. 

On Photon OS, `cloud-init` is enabled and running by default. You can use the following command to check the status: 
	
```
systemctl status cloud-init 
```

The Photon OS directory that contains the local data and other resources for cloud-init is `/var/lib/cloud`.

Photon OS stores the logs for cloud-init in the `/var/log/cloud-init.log` file.

The following sections demonstrate how to use cloud-init to customize a stand-alone Photon OS machine, instantiate a Photon OS machine in the Amazon EC2 cloud, and deploy a virtual machine running Photon OS in vSphere. Each section uses a different combination of the available options for the metadata and the user data that make up the data source. Specifications, additional options, and examples appear in the cloud-init documentation. 