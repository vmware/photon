Name:            photon-checksum-generator
Summary:         Userspace program to generate hmac sha256 / hmac sha512 sum of a file
Version:         1.2
Release:         2%{?dist}
License:         GPLv2+
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           Utilities
Source0:         https://github.com/vmware/photon-checksum-generator/%{name}-%{version}.tar.gz
%define sha1     %{name}=20658a922c0beca840942bf27d743955711c043a
BuildRequires:   gcc
Requires:        (linux-hmacgen or linux-secure-hmacgen or linux-aws-hmacgen or linux-esx-hmacgen)

%description
Userspace program to generate hmac-sha256/ hmac-sha512 sum of a file.
This module interacts with its kernel counterpart hmacgen device to generate the
shasum of a file.

%prep
%autosetup  -n %{name}-%{version}

%build
cd user
make all %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}%{_bindir}
cp user/hmacgen %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_sysconfdir}/hmacgen
touch %{buildroot}%{_sysconfdir}/hmacgen/hmacgen.conf

%files
%defattr(-,root,root)
%{_bindir}/hmacgen
%{_sysconfdir}/hmacgen/hmacgen.conf

%changelog
*   Thu Dec 9 2021 Vikash Bansal <bvikas@vmware.com> 1.2-2
-   Create "/etc/hmacgen/hmacgen.conf" to trigger initrd generation
*   Mon Mar 15 2021 Keerthana K <keerthanak@vmware.com> 1.2-1
-   Update to version 1.2
*   Wed Apr 29 2020 Keerthana K <keerthanak@vmware.com> 1.1-1
-   Update to version 1.1.
*   Tue Feb 11 2020 Keerthana K <keerthanak@vmware.com> 1.0-1
-   Initial photon checksum generator package for PhotonOS.
