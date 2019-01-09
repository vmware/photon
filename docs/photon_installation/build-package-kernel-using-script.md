# Building Package or Kernel Modules Using a Script

You can use a script to build individual packages or kernel modules. You place the sources and the specification files in the same folder and run the `build_spec.sh` script. The script installs all the build requirements from bintray. 

The `build-spec.sh` script is located in the `photon/tools/scripts/` folder.

- [Prerequisties](#prerequisites)
- [Procedure](#procedure)
- [Example](#example)
- [Build Logs](#build-logs)

## Prerequisites

Before you run the `build-spec.sh` script, perform the following steps:

- Place the source and specification files in the same folder.
- Copy the `build-spec.sh` script from the `photon/tools/scripts/` folder to the same folder as the source and specifications file.

## Procedure

Run the script as root user. Provide the specification file name as argument: 

```
./build_spec.sh <specification file name> 
```

The RPM or kernel module binary is generated in the same folder. 

## Example

The following example runs the script with `simple-module.spec` as argument, where `simple-module.spec` is the specification file:

```
./build_spec.sh simple-module.spec
```

The following are the contents of the `simple-module.spec` file:

```
Summary:        Simple Linux module
Name:           simple-module
Version:        4.18.9
Release:        5%{?dist}
License:    	GPLv2
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        module_example.tar.xz
BuildRequires:  linux-devel = 4.18.9
BuildRequires:  kmod
Requires:       linux = 4.18.9

%description
Example of building linux module for Photon OS

%prep
%setup -q -n module_example

%build
make -C `echo /usr/src/linux-headers-4.18.9*` M=`pwd` VERBOSE=1 modules %{?_smp_mflags}

%install
make -C `echo /usr/src/linux-headers-4.18.9*` M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
# fix permissins to generate non empty debuginfo
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%post
/sbin/depmod -a

%files
%defattr(-,root,root)
/lib/modules/*

```

## Build Logs

The followiing logs indicate the steps that the script performs internally:

```
1. Create sandbox
	Use local build template image OK
2. Prepare build environment
	Create source folder OK
	Copy sources from <HOME>/photon/tools/examples/build_spec/simple-module OK
	Install build requirements OK
3. Build
	Run rpmbuild OK
4. Get binaries
	Copy RPMS OK
	Copy SRPMS OK
5. Destroy sandbox
	Stop container OK
	Remove container OK

Build completed. RPMS are in '<HOME>/photon/tools/examples/build_spec/simple-module/stage' folder
```

