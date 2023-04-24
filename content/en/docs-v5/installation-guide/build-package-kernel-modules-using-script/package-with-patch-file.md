---
title:  Include a patch file
weight: 4
---

This example shows how to build a package with a patch file. To build the package, you need to run the script with `python-M2Crypto.spec` as  an argument, where `python-M2Crypto.spec` is the RPM specification file.

You can find the patch file at the following location: 

```
https://github.com/vmware/photon/tree/<BRANCH>/tools/examples/build_spec/user_package_example/0001-openssl-3.0.0-support.patch
```

To generate the output in the spec-file folder, run the following command:

```
./photon/tools/scripts/build_spec.sh ./photon/tools/examples/build_spec/user_package_example/python-M2Crypto.spec
```


The following are the contents of the `python-M2Crypto.spec` file:

```
Name:           python3-M2Crypto
Version:        0.36.0
Release:        1%{?dist}
Summary:        Crypto and SSL toolkit for Python
Group:          Development/Languages/Python
License:        MIT
URL:            https://pypi.python.org/pypi/M2Crypto/0.26.0
Source0:        https://pypi.python.org/packages/11/29/0b075f51c38df4649a24ecff9ead1ffc57b164710821048e3d997f1363b9/M2Crypto-%{version}.tar.gz
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing
BuildRequires:  swig
BuildRequires:  python3-xml
Requires:       python3-typing
Requires:       python3
Requires:       openssl
Patch0:         0001-openssl-3.0.0-support.patch

%description
M2Crypto is a crypto and SSL toolkit for Python featuring the following:

RSA, DSA, DH, HMACs, message digests, symmetric ciphers (including
AES). SSL functionality to implement clients and servers. HTTPS
extensions to Python's httplib, urllib, and xmlrpclib. Unforgeable
HMAC'ing AuthCookies for web session management. FTP/TLS client and
server. S/MIME. ZServerSSL: A HTTPS server for Zope. ZSmime: An S/MIME
messenger for Zope.

%prep
# Using autosetup is not feasible
%setup -q -n M2Crypto-%{version}
%patch0 -p1

%build
CFLAGS="%{optflags}" python3 setup.py build --openssl=/usr/include --bundledlls

%install
rm -rf %{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*
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
        Download M2Crypto-0.36.0.tar.gz OK
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
Build completed. RPMS are in './photon/tools/examples/build_spec/user_package_example/stage' folder
```
