---
title: Hello World Binary
weight: 2
---

This example shows how to build a package that provides a hello world binary. To build the package, you need to run the script with `hello-world-user1.spec` as an argument, where `hello-world-user1.spec` is the RPM specification file.

You can find the source file at the following location:  

```
https://github.com/vmware/photon/tree/<BRANCH>/tools/examples/build_spec/user_package_example/hello-world-user1.tar.gz
```

To generate the output in a staging directory, run the following command:

```
./photon/tools/scripts/build_spec.sh ./photon/tools/examples/build_spec/user_package_example/hello-world-user1.spec $STAGEDIR
```

The following are the contents of the `hello-world-user1.spec` file:

```
% Summary:      Hello World User Package
Name:           hello-world-user1
Version:        1.0
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        hello-world-user1.tar.gz

%description
Example of building User Package for Photon OS

%prep
%autosetup -n hello-world-user1

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
/usr/bin/*
```

#### Build Logs

The following logs indicate the steps that the script performs internally:

```
0. Build Script Version: 1.1
1. Create sandbox
        Use local build template image OK
2. Prepare build environment
        Create source folder OK
        Copy sources from ./photon/tools/examples/build_spec/user_package_example OK
        install createrepo OK
        createrepo  OK
        Create local repo in sandbox OK
        makecache OK
        Install build requirements OK
3. Build Binary and Source Package
        Run rpmbuild OK
        Delete SOURCES OK
4. Destroy sandbox
        Stop container OK
        Remove container OK
Build completed. RPMS are in '$STAGEDIR' folder
```


#### Verification

You can verify the generated output with the following commands:


- Command to install the RPM:

```
rpm -ivh $STAGEDIR/RPMS/x86_64/hello-world-user-1.0-1.ph5.x86_64.rpm
```

- Command to verify the installed user package (execute the installed binary of the user package):

```
root@photon-aab77099dca0root [ ~ ]# /usr/bin/hello-world-user
     Hello World
```