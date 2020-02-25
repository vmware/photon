Name:            photon-checksum-generator
Summary:         Userspace program to generate hmac sha256 / hmac sha512 sum of a file
Version:         1.0
Release:         1%{?dist}
License:         GPLv2+
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Utilities
Source0:         https://github.com/vmware/photon-checksum-generator/%{name}-%{version}.tar.gz
%define sha1     %{name}=b2a0528ce733e27bf332ea533072faf73c336f0c
BuildRequires:   gcc
Requires:        (linux-hmacgen or linux-secure-hmacgen or linux-aws-hmacgen or linux-esx-hmacgen)

%description
Userspace program to generate hmac-sha256/ hmac-sha512 sum of a file.
This module interacts with its kernel counterpart hmacgen device to generate the
shasum of a file.

%prep
%setup -q -n %{name}-%{version}

%build
cd user
make all

%install
install -vdm 755 %{buildroot}%{_bindir}
cp user/hmacgen %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%{_bindir}/hmacgen

%changelog
*   Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 1.0-1
-   Initial photon checksum generator package for PhotonOS.
