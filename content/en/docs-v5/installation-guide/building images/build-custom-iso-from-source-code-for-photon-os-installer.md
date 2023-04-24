---
title:  Build a Custom ISO from the Source Code of Photon OS Installer	
weight: 8
---

The `custom-iso` tool allows you to build images as per your requirements. 

[Overview](#Overview)  
[Prerequisite](#prerequisite)  
[Preparing for Custom Image Generation](#preparing-for-custom-image-generation)   
[Generating a Custom Image](#generating-a-custom-image)  


## Overview
You can use the `custom-iso` tool to create images such as a custom `ISO`, `Initrd`, and `RPM-OSTree`. To generate an image, you must provide the necessary inputs in the form of arguments. The `custom-iso` tool creates images based on the inputs you provide.

You can use the following functions to generate the required images:

- `build-initrd` generates a custom Initrd image

- `build-initrd` generates a custom ISO image.

- `build-rpm-ostree-iso` generates a custom RPM-OSTree ISO.

As an input to the tool, you must provide the list of all the necessary packages for the custom ISO in a JSON file. The tool only uses the minimal list of packages and their dependencies that you specify.

You can customize the following files and configurations:

- List of packages to install
- Kickstart file
- Boot command line
- Repo to download the packages
- Installer `initrd` package list
- Custom ostree tar archive

Note that when you use the Custom ISO builder to build the `ISO` and the Installer `initrd`, the `ISO` and `initrd` files are generated with the following naming conventions:

- ISO: `photon-<photon-release-version>.iso`

- Initrd: `initrd.img`

## Prerequisite

To generate a custom ISO, ensure that you provide the following required parameters:

- List of custom packages in JSON format
- Photon Release Version
- Generating Function: For example, `build-iso`, `build-initrd`, and `build-rpm-ostree-iso`
- Path to OSTree tar archive (required only if function is set to `build-rpm-ostree-iso`)

**Note**: You must provide the additional repository if you want to include a package that the Photon OS official repository does not provide.

You can also provide the following optional parameters:

- Custom Kickstart file
- Additional repositories
- Boot command line parameters
- Custom `Initrd` package list file
- Artifact path


## Preparing for Custom Image Generation

1. Install the following prerequisite packages:

	- python3-pip
	- git
	- tar
	- createrepo_c
	- binutils
	- dosfstools
	- cdrkit
	- docker

	*i*. To install the specified packages on Photon OS, use the following command: 
	```
	tdnf install -y python3-pip git tar createrepo_c binutils dosfstools cdrkit
	``` 

2. Run following command to install photon-os-installer python library:

	```
	pip3 install git+https://github.com/vmware/photon-os-installer.git
	```   

3. Enable the following services before you build the custom `iso`/`initrd`: `docker`
	
	i. To enable the docker service and log in to the docker account, use the following command:	
	
	```
	systemctl start docker.service;
	docker login # To avoid docker pull rate limit
	```   

4. Create the file containing the custom package list.

	The following list shows some of the sample custom package files:
	- Sample custom package file for an ISO: [packages_minimal.json](https://github.com/vmware/photon/blob/5.0/common/data/packages_minimal.json)
	- Sample initrd package list file: [packages_installer_initrd.json](https://github.com/vmware/photon/blob/5.0/common/data/packages_installer_initrd.json)

	Package list json format-
	```
	{
    "packages": <list-of-pkgs>,
    "packages_x86_64": <x86-specific-pkgs>,
    "packages_aarch64": <aarch64-specific-pkgs>
	}
	```    	

For more details, refer to the following link: https://github.com/vmware/photon-os-installer/blob/master./ks_config.md#packages-optional-if-packagelist_file-set

**Note**: `packages_x86_64` and `packages_aarch64` are optional keys. The `packages_minimal.json` file is a sample file. You can create your own JSON file with the list of custom packages that you want, and provide the directory path for the file in the command to generate the `iso`/`initrd`.


  
## **Generating a Custom Image**


You can use the respective commands to generate the custom images for the following use cases.

  
<details><summary>Using Package List</summary>
<p>

Command:

```
photon-iso-builder -v <photon-release-version> -p <path/to/custom-package-list-json>
```  
Example:
```
photon-iso-builder -v 5.0 -p /root/packages_custom.json
```       


**Note**: you can skip the `--function` invocation because `photon-iso-builder` sets the default function to `build-iso`.

</p>
</details>


<details><summary>Using Package List and Additional Repository</summary>
<p>


```
photon-iso-builder -v <photon-release-version> -p <path/to/custom-package-list-json> [-r <path/to/custom-repo-list>]
```   
Example:
```
photon-iso-builder -v 5.0 -p /root/packages_custom.json -r local.repo -r local2.repo
```   

**Note**: In order to create your own custom repository, see the following page: [Adding a New Repository](https://vmware.github.io/photon./administration-guide/managing-packages-with-tdnf/adding-a-new-repository/)

</p>
</details>





<details><summary>Using Custom Kickstart File</summary>
<p>

Command:	
```
photon-iso-builder -v <photon-release-version> -p <path/to/custom-package-list-json> -k <path-to-kickstart>
```   

Example:
```
photon-iso-builder -v 5.0 -p /root/packages_custom.json -k /root/custom_kickstart.json
```   

To create a custom kickstart configuration file, see the follow page: [Kickstart Configuration](https://github.com/vmware/photon-os-installer/blob/master./ks_config.md)  

**Note**: If the Kickstart file is provided while creating the custom ISO, boot command line parameter is not edited to install the ISO through kickstart.
	
To boot the ISO through the provided kickstart file, you need to create the custom ISO file using the following format:

```
photon-iso-builder -v <photon-release-version> -p <path/to/custom-package-list-json> -f build-iso -k <path-to-kickstart> -b "ks=cdrom:/isolinux/<kickstart-file-base-name>"
```   
Example:
```
photon-iso-builder -v 5.0 -p /root/packages_custom.json -k /root/custom_kickstart.json -b "ks=cdrom:/isolinux/custom_kickstart.json"
```
</p>
</details>





<details><summary>Using Extra Boot Command Line Parameters</summary>
<p>

Command:
```
photon-iso-builder -v <photon-release-version> -p <path/to/custom-package-list-json> -f build-iso -b <extra-boot-parameter>
```   

Example:
```
photon-iso-builder -v 5.0 -p /root/packages_custom.json -b "ks=http://10.197.102.86:8000/sample_ks.cfg insecure_installation=1"
```    
</p>
</details>



<details><summary>Using Default Installation as RPM-OStree</summary>
<p>

Before you generate the custom image using default installation as RPM-OStree, you need to generate ostree tar archive. Perform the following steps to generate the ostree tar archive:

1. Generate the ostree repo tree as directed here: [Creating a Server](https://vmware.github.io/photon./administration-guide/photon-rpm-ostree/creating-a-rpm-ostree-server/)

2. Create tarball of the repo tree:

	Command:
```
	tar -czf </path/to/>ostree-repo.tar.gz -C </path/to/repotree>/repo
```   

Example: repo tree resides inside the following directory my-repo like `/root/my-repo/repo`
    
```   
	tar -zcf /root/ostree-repo.tar.gz -C /root/my-repo/repo .
```    

Once the tar archive is generated, generate the custom image.
To generate the custom image using default installation as RPM-OStree, execute the following command:



```
photon-iso-builder -v <photon-release-version> -o <path/to/ostree-tar-archive> -f build-rpm-ostree-iso
```

Example:
```
photon-iso-builder -v 5.0 -o /root/ostree-repo.tar.gz -f build-rpm-ostree-iso
```
**Note**: You can either provide a local path or a URL for the ostree tar archive. Custom package list json is not required for this case.

</p>
</details>





<details><summary>Using Custom Artifact Path</summary>
<p>


Command:
```
photon-iso-builder -v <photon-release-version> -p <path/to/custom-package-list-json> -a <custom-artifact-path>
```
**Note**: Custom artifact path parameter takes parent directory path as the input in which the artifact is placed.

As per the user input, artifact is placed under `/root/custom/path` in the following example:
```
photon-iso-builder -v 5.0 -p /root/packages_custom.json -a /root/custom/path
```
</p>
</details>





<details><summary>Custom Initrd</summary>
<p>


Command:
```
photon-iso-builder -v <photon-release-version> -c <path/to/custom-initrd-pkg-list-file> -f build-initrd
```   
Example:
```
photon-iso-builder -v 5.0 -c /root/packages_custom_initrd.json -f build-initrd
```

The default initrd package list file is located in the following directory: https://github.com/vmware/photon/blob/master/common/data/packages_installer_initrd.json

</p>
</details>



## Generating custom ISO through source code:

The following command demonstrate how to generate a custome ISO through the source code:

```
git clone https://github.com/vmware/photon-os-installer.git
cd photon-os-installer/photon_installer
./isoBuilder -v 5.0 -p packages_minimal.json
```

	
	
	




