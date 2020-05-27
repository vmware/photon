# Examining the Packages in the SPECS Directory on Github

The SPECS directory of the GitHub website for Photon OS contains all the packages that can appear in Photon OS repositories. The following is the path to the SPECS directory :  

`https://github.com/vmware/photon/tree/master/SPECS`

To see the version of a package, in the SPECS directory, click the name of the subdirectory of the package that you want to examine, and then click the `.spec` filename in the subdirectory. 

For example, the version of OpenJDK, which contains the openjre package that installs the Java class library and the javac Java compiler appears as follows:

```
%define _use_internal_dependency_generator 0
Summary:	OpenJDK 
Name:		openjdk
Version:	1.8.0.72
Release:	1%{?dist}
License:	GNU GPL
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
AutoReqProv: 	no
Source0:	http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-%{version}/OpenJDK-%{version}-x86_64-bin.tar.xz
%define sha1 OpenJDK=0c705d7b13f4e22611d2da654209f469a6297f26
%description
The OpenJDK package installs java class library and javac java compiler. 

%package	-n openjre
Summary:	Jave runtime environment
AutoReqProv: 	no
%description	-n openjre
It contains the libraries files for Java runtime environment
#%global __requires_exclude ^libgif.*$
#%filter_from_requires ^libgif.*$...
```


