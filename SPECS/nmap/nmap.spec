Summary:        Nmap (“Network Mapper”) is a utility for network discovery and security auditing
Name:           nmap
Version:        7.93
Release:        3%{?dist}
License:        Nmap
URL:            http://nmap.org
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://nmap.org/dist/%{name}-%{version}.tar.bz2
%define sha512 %{name}=4ec9295e25bd7a215e718c3dbbf09bfe6339b60850f4a8d09b5ad0cbf41a0da8ece0168efc5ca91ba1ecbd83b1d31735d77dacd5f1ec1a9fd212454dd1f0f0fd

BuildRequires:  build-essential
BuildRequires:  e2fsprogs-devel
BuildRequires:  gettext
BuildRequires:  gnupg
BuildRequires:  gpgme-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libgpg-error
BuildRequires:  libpcap-devel
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel
BuildRequires:  lua-devel

Requires:       libpcap
Requires:       pcre
Requires:       gnupg
Requires:       lua
Requires:       openssl
Requires:       zlib
Requires:       libgcc

%description
nmap is a utility for network exploration or security auditing. It supports
ping scanning (determine which hosts are up), many port scanning techniques
(determine what services the hosts are offering), and TCP/IP fingerprinting
(remote host operating system identification). Nmap also offers flexible target
and port specification, decoy scanning, determination of TCP sequence
predictability characteristics, reverse-identd scanning, and more. In addition
to the classic command-line nmap executable, the Nmap suite includes a flexible
data transfer, redirection, and debugging tool (netcat utility ncat), a utility
for comparing scan results (ndiff), and a packet generation and response
analysis tool (nping)

%package ncat
Summary: Nmap's Netcat replacement
Provides: nc
Provides: nc6

%description ncat
Ncat is a feature packed networking utility which will read and
write data across a network from the command line.  It uses both
TCP and UDP for communication and is designed to be a reliable
back-end tool to instantly provide network connectivity to other
applications and users. Ncat will not only work with IPv4 and IPv6
but provides the user with a virtually limitless number of potential
uses.

%prep
%autosetup -p1

%build
%configure \
    --with-libpcap=%{_prefix} \
    --with-liblua=%{_prefix} \
    --without-zenmap \
    --without-ndiff \
    --enable-dbus

%make_build

%install
%make_install STRIP=true %{?_smp_mflags}

rm -rf %{buildroot}%{_datadir}/man/ \
       %{buildroot}%{_datadir}/ncat/

%files
%defattr(-,root,root)
%{_bindir}/nmap
%{_bindir}/nping
%{_datadir}/nmap

%files ncat
%defattr(-,root,root)
%{_bindir}/ncat

%changelog
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 7.93-3
- Bump version as a part of gettext upgrade
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 7.93-2
- Bump release as a part of libgpg-error upgrade to 1.46
* Fri Nov 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 7.93-1
- Upgrade to v7.93
* Mon May 30 2022 Gerrit Photon <photon-checkins@vmware.com> 7.92-1
- Automatic Version Bump
* Wed Apr 28 2021 Susant Sahani <ssahani@vmware.com> 7.91-1
- Initial rpm release
