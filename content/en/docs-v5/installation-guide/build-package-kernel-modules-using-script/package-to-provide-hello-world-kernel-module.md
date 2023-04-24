---
title:  Hello World Kernel Module
weight: 1
---

This example shows how to build a package that provides a hello world kernel module. To build the package, you need to run the script with `hello-world.spec` as an argument, where `hello-world.spec` is the RPM specification file.

You can find the source file at the following location:  

	https://github.com/vmware/photon/tree/<BRANCH>/tools/examples/build_spec/kernel_module_example/hello-world.tar.gz	

To generate the output in the spec-file folder, run the following command:


	./photon/tools/scripts/build_spec.sh ./photon/tools/examples/build_spec/kernel_module_example/hello-world.spec

The following are the contents of the `hello-world.spec` file:

```
%define linux_esx_ver 6.1.10

Summary:        Hello World Linux module
Name:           hello-world
Version:        1.0
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        hello-world.tar.gz
BuildRequires:  linux-esx-devel = %{linux_esx_ver}
BuildRequires:  kmod
Requires:       linux-esx = %{linux_esx_ver}

%description
Example of building linux module for Photon OS

%prep
%autosetup -n hello-world

%build
make -C `echo /usr/src/linux-headers-%{linux_esx_ver}*` M=`pwd` VERBOSE=1 modules %{?_smp_mflags}

%install
make -C `echo /usr/src/linux-headers-%{linux_esx_ver}*` M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install %{?_smp_mflags}
# fix permissins to generate non empty debuginfo
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ldconfig_scriptlets

%post
/sbin/depmod -a

%files
%defattr(-,root,root)
/lib/modules/*

```

#### Build Logs

The following logs indicate the steps that the script performs internally:

```

0. Build Script Version: 1.1
1. Create sandbox
        Use local build template image OK
2. Prepare build environment
        Create source folder OK
        Copy sources from ./photon/tools/examples/build_spec/kernel_module_example OK
        install createrepo OK
        createrepo  OK
        Create local repo in sandbox OK
        makecache OK
3. Build Binary and Source Package
        Run rpmbuild OK 
        Delete SOURCES OK
4. Destroy sandbox 
        Stop container OK
        Remove container OK
Build completed. RPMS are in './photon/tools/examples/build_spec/kernel_module_example/stage' folder

```


#### Verification

You can verify the generated output with the following commands:

- Command to install the RPM:  
   
```
rpm -ivh ./photon/tools/examples/build_spec/kernel_module_example/stage/RPMS/x86_64/hello-world-1.0-1.ph5.x86_64.rpm
```



- Command to install the kernel module:
```
modprobe hello-world
```




- Command to verify the installed kernel module:

```
dmesg | grep "Hello World"
```