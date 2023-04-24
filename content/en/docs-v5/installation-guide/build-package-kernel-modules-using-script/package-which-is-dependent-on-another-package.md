---
title:  Manage a Dependent package
weight: 3
---

This example shows how to build a dependent package. To build the package, you need to run the script with `hello-world-user.spec` as an argument, where `hello-world-user.spec` depends on the RPM build from `hello-world-user1.spec` (`hello-world-user -> hello-world-user1`)

You can find the source file at the following location: 

```
https://github.com/vmware/photon/tree/<BRANCH>/tools/examples/build_spec/user_package_example/hello-world-user.tar.gz
```

To generate the output in a staging directory, run the following command:

```
./photon/tools/scripts/build_spec.sh ./photon/tools/examples/build_spec/user_package_example/hello-world-user.spec $STAGEDIR
```

The following are the contents of the `hello-world-user.spec` file:

```
Summary:        Hello World User Package
Name:           hello-world-user
Version:        1.0
Release:        1%{?dist}
License:        GPLv2
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        hello-world-user.tar.gz
BuildRequires:  hello-world-user1
BuildRequires:  git
Requires:       hello-world-user1

%description
Example of building User Package for Photon OS

%prep
%autosetup -n hello-world-user

%build
make %{?_smp_mflags}

%install
pwd
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
/usr/bin/*
```


## Build Logs

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
Build completed. RPMS are in '$STAGEDIR' folder.
```