Summary:        Nmap (“Network Mapper”) is a utility for network discovery and security auditing
Name:           nmap
Version:        7.91
Release:        1%{?dist}
License:        Nmap
URL:            http://nmap.org/
Source0:        https://nmap.org/dist/%{name}-%{version}.tar.bz2
%define sha1 nmap=e72198f463ee9d557e4c5c9444cc5a0e5c36b00c
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  e2fsprogs-devel
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gnupg
BuildRequires:  gpgme-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libgpg-error
BuildRequires:  libpcap-devel
BuildRequires:  make
BuildRequires:  openssh
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel

Requires:       libpcap
Requires:       pcre
Requires:       gnupg

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
%configure  --with-libpcap=yes --with-liblua=included \
            --without-zenmap --without-ndiff \
            --enable-dbus

%install
make DESTDIR=%{buildroot} STRIP=true install

rm -f %{buildroot}%{_datadir}/ncat/ca-bundle.crt
rmdir %{buildroot}%{_datadir}/ncat
rm -rf %{buildroot}%{_datadir}/man/

%files
%defattr(-,root,root)
%license LICENSE
%doc docs/README
%doc docs/nmap.usage.txt
%{_bindir}/nmap
%{_bindir}/nping
%{_datadir}/nmap

%files ncat
%license LICENSE
%doc ncat/docs/AUTHORS ncat/docs/README ncat/docs/THANKS ncat/docs/examples
%{_bindir}/ncat

%changelog
* Wed Apr 28 2021 Susant Sahani <ssahani@vmware.com> 7.91-1
- Initial rpm release
