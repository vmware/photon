# Configure a Repository

Photon OS comes with a preconfigured repository called `photon-iso` that resides in `\etc\yum.repos.d.` If you receive an access error message when working with the `photon-iso` repository, it is probably because you do not have the Photon OS ISO mounted. Mount the ISO and the run the following command to update the metadata for all known repositories, including `photon-iso`: 

	mount /dev/cdrom /media/cdrom
	tdnf makecache
	
	Refreshing metadata for: 'VMware Lightwave 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)Updates'
	Refreshing metadata for: 'VMware Photon Extras 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)'
	Metadata cache created.
