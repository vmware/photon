%global commit_id 1270245

Summary:        OpenBSD netcat to read and write data across connections using TCP or UDP
Name:           netcat
# Version obtained from netcat.c header comment
Version:        1.228
Release:        1%{?dist}
# BSD-3-Clause: nc.1 and netcat.c
# BSD-2-Clause: atomicio.{c,h} and socks.c
License:        BSD-3-Clause AND BSD-2-Clause
URL:            https://man.openbsd.org/nc.1
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

# Steps to create tarball:
# https://github.com/openbsd/src/tree/master/usr.bin/nc
# git clone https://github.com/openbsd/src.git --depth 1
# Get commit id of 'usr.bin/nc' directory from upstream
# mv src/tree/master/usr.bin/nc nc-<commit_id>
# Example:
# mv src/tree/master/usr.bin/nc nc-1270245
# tar cJF nc-1270245.tar.xz nc-1270245
Source0: https://packages.vmware.com/photon/photon_sources/1.0/nc-%{commit_id}.tar.xz
%define sha512 nc-%{commit_id}=e3e4399fd917db2b0704a0f573a0ec81d82e64071461825e2cae939dbbfacc52b5dad448a821b3699217b305a68a265fd8f4a15a185f694f081272460c251469

Patch0: 0001-Port-to-linux-with-libbsd.patch
Patch1: 0002-add-unveil-pledge-macros.patch
Patch2: 0003-add-ltls-link-flag.patch

BuildRequires: libretls-devel
BuildRequires: libbsd-devel

Requires: libretls
Requires: libbsd

%description
The OpenBSD nc (or netcat) utility can be used for just about anything involving
TCP, UDP, or UNIX-domain sockets. It can open TCP connections, send UDP packets,
listen on arbitrary TCP and UDP ports, do port scanning, and deal with both IPv4
and IPv6. Unlike telnet(1), nc scripts nicely, and separates error messages onto
standard error instead of sending them to standard output, as telnet(1) might do
with some.

%prep
%autosetup -p1 -n nc-%{commit_id}

%build
%make_build

%install
install -D -p -m 0755 nc %{buildroot}%{_bindir}/%{name}
ln %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/nc

%files
%defattr(-,root,root)
%{_bindir}/nc
%{_bindir}/%{name}

%changelog
* Tue Sep 10 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.228-1
- Switch to BSD netcat.
- GNU netcat-0.7.1 was released back in Jan 2004.
* Thu Oct 19 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-5
- Remove infodir
- Use standard build macros
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-4
- Use standard configure macros
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 0.7.1-3
- Removed packaging of debug files
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.1-2
- GA - Bump release of all rpms
* Tue Dec 08 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.7.1-1
- Initial build.    First version
