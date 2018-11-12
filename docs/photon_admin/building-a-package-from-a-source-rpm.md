# Building a Package from a Source RPM

This section describes how to install and build a package on the full version of Photon OS from the package's source RPM. You obtain the source RPMs that Photon OS uses from Bintray: 

[https://bintray.com/vmware/photon](https://bintray.com/vmware/photon)

To build a package from its source RPM, or SRPM, Photon OS requires the following packages:  

* rpmbuild. This package is installed by default on the full version of Photon OS, so you should not have to install it. 
* gcc. This package is also installed by default on the full version of Photon OS, so you should not have to install it. 
* make, Cmake, automake, or another make package, depending on the package you are trying to install and build from its source RPM. Cmake is installed by default on Photon OS. You can install other make packages if need be by using tdnf or yum.  

Another requirement is a local unprivileged user account other than the root account. You should build RPMs as an unprivileged user. Do not build a package as root--building an RPM with the root account might damage your system. 

If you are building a package on a virtual machine running Photon OS in VMware vSphere, VMware Workstation, or VMware Fusion, take a snapshot of your virtual machine before building the package. 

VMware recommends that you install and build packages from their source RPMs on the full version of Photon OS. Do not use the minimal version to work with source RPMs.  

Here's how to install and build an example package--sed, in this case--from its source RPM on Photon OS with an unprivileged account. 

First, check whether rpmbuild is installed by running the following command: 

	rpmbuild --version

If it is not installed, install it by running the following command as root: 

	tdnf install rpm-build

Second, create the directories for building RPMs under your local user account's home directory (not under root):

	mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

Next, create a .rpmmacros file under your home directory and override the default location of the RPM building tree with the new one. This command overwrites an existing .rpmmacros file. Before running the following command, make sure you do not already have a .rpmmacros file; if a .rpmmacros file exists, back it up under a new name in case you want to restore it later. 

	echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

Now place the source RPM file that you want to install and build in the /tmp directory. 

To install the source file, run the following command with your unprivileged user account, replacing the sed example source RPM with the name of the one that you want to install: 

	rpm -i /tmp/sed-4.2.2-2.ph1.src.rpm

The above command unpacks the source RPM and places its .spec file in your ~/rpmbuild/SPECS directory. In the next step, the rpmbuild tool uses the .spec file to build the RPM. 

To build the RPM, run the following commands with your unprivileged user account. Again, replace the sed.spec example file with the name of the .spec file that you want to build. 

	cd ~/rpmbuild/SPECS
	rpmbuild -ba sed.spec

If successful, the rpmbuild -ba command builds the RPM and generates an RPM package file in your ~/rpmbuild/RPMS/x86_64 directory. Example:

	ls RPMS/x86_64/
	sed-4.2.2-2.x86_64.rpm  sed-debuginfo-4.2.2-2.x86_64.rpm  sed-lang-4.2.2-2.x86_64.rpm

The rpmbuild command also generates a new SRPM file and saves it in your ~/rpmbuild/SRPMS directory. Example:  

	ls SRPMS/
	sed-4.2.2-2.src.rpm

If the rpmbuild command is unsuccessful with an error that it cannot find a library, you must install the RPMs for the library that your source RPM depends on before you can successfully build your source RPM. Iterate through installing the libraries that your source RPM relies on until you can successfully build it. 

To install the RPM, run the following command with your unprivileged user account:  

	rpm -i RPMS/x86_64/sed-4.2.2-2.x86_64.rpm