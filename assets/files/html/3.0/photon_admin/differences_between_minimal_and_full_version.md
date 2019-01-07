# Looking at the Differences Between the Minimal and the Full Version

The minimal version of Photon OS contains around 50 packages. As it is installed, the number of packages increases to nearly 100 to fulfill dependencies. The full version of Photon OS adds several hundred packages to those in the minimal version to deliver a more fully featured operating system. 

You can view a list of the packages that appear in the minimal version by examining the following file: 

[https://github.com/vmware/photon/blob/master/common/data/packages_minimal.json](https://github.com/vmware/photon/blob/master/common/data/packages_minimal.json)

You can view a list of the packages that appear in the full version by examining the following file: 

[https://github.com/vmware/photon/blob/master/common/data/packages_full.json](https://github.com/vmware/photon/blob/master/common/data/packages_full.json)

If the minimal or the full version of Photon OS does not contain a package that you want, you can install it with tdnf, which appears in both the minimal and full versions of Photon OS by default. In the full version of Photon OS, you can also install packages by using yum. 

One notable difference between the two versions of Photon OS pertains to OpenJDK, the package that contains not only the Java runtime environment (`openjre`) but also the Java compiler (`javac`). The OpenJDK package appears in the full but not the minimal version of Photon OS. 

To add support for Java programs to the minimal version of Photon OS, install the Java packages and their dependencies by using the following command: 

	tdnf install openjdk
	Installing:
	openjre 	x86_64    1.8.0.92-1.ph1    95.09 M
	openjdk 	x86_64    1.8.0.92-1.ph1    37.63 M

**NOTE:** `openjdk` and `openjre` are available as openjdk8 and openjre8 in Photon OS 2.0

For more information about `tdnf`, see [Tiny DNF for Package Management](tiny-dnf-for-package-management.md)
