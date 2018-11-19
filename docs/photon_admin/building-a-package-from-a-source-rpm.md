# Building a Package from a Source RPM

This section describes how to install and build a package on the full version of Photon OS from the package's source RPM. Obtain the source RPMs that Photon OS uses from the  Bintray location, [https://bintray.com/vmware/photon](https://bintray.com/vmware/photon)


## Prerequisites

- To build a package from its source RPM, or SRPM, Photon OS requires the following packages:  

    * `rpmbuild`. This package is installed by default on the full version of Photon OS, so you should not have to install it. 
    * `gcc`. This package is also installed by default on the full version of Photon OS, so you should not have to install it. 
    * `make`, `Cmake`, `automake`, or another `make` package, depending on the package you are trying to install and build from its source RPM. Cmake is installed by default on Photon OS. 
        
        You can install other make packages by using tdnf or yum.  
- A local unprivileged user account other than the root account. You should build RPMs as an unprivileged user. Do not build a package as `root` becau--building an RPM with the root account might damage your system. 
- Take a snapshot of your virtual machine before building the package if you are building a package on a virtual machine running Photon OS in VMware vSphere, VMware Workstation, or VMware Fusion.


## Procedure

VMware recommends that you install and build packages from their source RPMs on the full version of Photon OS. Do not use the minimal version to work with source RPMs.  

Perfrom the following steps to install and build an example package- `sed` from its source RPM on Photon OS with an unprivileged account. 

1. check whether rpmbuild is installed by running the following command: 
	
    ```
    rpmbuild --version
```
    If it is not installed, install it by running the following command as root: 
	
    ```
    tdnf install rpm-build
```

1. Create the directories for building RPMs under your local user account home directory and not under root:
	
    ```
    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
```

1. Create a `.rpmmacros` file under your home directory and override the default location of the RPM building tree with the new one. This command overwrites an existing `.rpmmacros` file. Before running the following command, make sure you do not already have a `.rpmmacros file`. If a `.rpmmacros` file exists, back it up under a new name in case you want to restore it later.    

    ```
echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros
```

1. Place the source RPM file that you want to install and build in the `/tmp` directory. 
1. Install the source file, run the following command with your unprivileged user account, replacing the sed example source RPM with the name of the one that you want to install: 

	
    ```
    rpm -i /tmp/sed-4.2.2-2.ph1.src.rpm
    ```

    The above command unpacks the source RPM and places its `.spec` file in your `~/rpmbuild/SPECS` directory. In the next step, the `rpmbuild` tool uses the `.spec` file to build the RPM. 
1. Build the RPM, run the following commands with your unprivileged user account. Replace the `sed.spec` example file with the name of the `.spec` file that you want to build. 
	
    ```
    cd ~/rpmbuild/SPECS
	rpmbuild -ba sed.spec
```

    If successful, the rpmbuild -ba command builds the RPM and generates an RPM package file in your ~/rpmbuild/RPMS/x86_64 directory. For example:
	
    ```
    ls RPMS/x86_64/
	sed-4.2.2-2.x86_64.rpm  sed-debuginfo-4.2.2-2.x86_64.rpm  sed-lang-4.2.2-2.x86_64.rpm
```

    The rpmbuild command also generates a new SRPM file and saves it in your ~/rpmbuild/SRPMS directory. For example:  

    ```
    ls SRPMS/
	sed-4.2.2-2.src.rpm
```

    If the rpmbuild command is unsuccessful with an error that it cannot find a library, you must install the RPMs for the library that your source RPM depends on before you can successfully build your source RPM. Iterate through installing the libraries that your source RPM relies on until you can successfully build it. 

1. To install the RPM, run the following command with your unprivileged user account:  
	
    ```
rpm -i RPMS/x86_64/sed-4.2.2-2.x86_64.rpm
```
