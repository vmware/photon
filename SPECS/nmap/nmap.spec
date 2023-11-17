Summary:        Nmap (“Network Mapper”) is a utility for network discovery and security auditing
Name:           nmap
Version:        7.91
Release:        4%{?dist}
License:        Nmap
URL:            http://nmap.org/
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://nmap.org/dist/%{name}-%{version}.tar.bz2
%define sha512 %{name}=9d59f031b5f748311e9f9a0b9d05ad4a7a70fc6ac17598d7c4c81a4825c95d53817d74435d839e67b9379a052f2d37889fd634f9c75301a851f465d60fb9974d

BuildRequires: e2fsprogs-devel
BuildRequires: build-essential
BuildRequires: gettext
BuildRequires: gnupg
BuildRequires: gpgme-devel
BuildRequires: krb5-devel
BuildRequires: libcap-devel
BuildRequires: libpcap-devel
BuildRequires: libgpg-error
BuildRequires: openssh
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: lua-devel

Requires: libpcap
Requires: pcre
Requires: gnupg

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
Provides: nc nc6

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
    --with-libpcap=%{_usr} \
    --with-liblua=%{_usr} \
    --without-zenmap \
    --without-ndiff \
    --enable-dbus

%make_build

%install
%make_install %{?_smp_mflags} STRIP=true

rm -f %{buildroot}%{_datadir}/ncat/ca-bundle.crt
rmdir %{buildroot}%{_datadir}/ncat
rm -rf %{buildroot}%{_datadir}/man/

%files
%defattr(-,root,root)
%{_bindir}/nmap
%{_bindir}/nping
%{_datadir}/nmap

%files ncat
%defattr(-,root,root)
%{_bindir}/ncat

%changelog
* Fri Nov 10 2023 Prashant S Chauhan <sshedi@vmware.com> 7.91-4
- Use system provided lua
* Fri Jul 28 2023 Shivani Agarwal <shivania2@vmware.com> 7.91-3
- Bump version as part of openssh upgrade
* Tue Nov 30 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.91-2
- Increment for openssl 3.0.0 compatibility
* Wed Apr 28 2021 Susant Sahani <ssahani@vmware.com> 7.91-1
- Initial rpm release
