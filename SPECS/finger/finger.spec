Summary:        The finger client
Name:           finger
Version:        0.17
Release:        4%{?dist}
URL:            https://github.com/Distrotech/bsd-finger
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/bsd-finger-%{version}.tar.gz
%define sha512 bsd-finger=07570a9a5797579273938ef728f222f483c733e78eb6acb00e2bce9ff9df29aa85ed715872032701c8f67fcbc7cf5501f12dc2b8234c30df7d25f50cc38359b0
Source1:        finger.socket
Source2:        finger@.service
Source3:        LICENSE

Source4: license.txt
%include %{SOURCE4}

Patch0:         bsd-finger-time.patch
Patch1:         fix-manpage-typo.patch
BuildRequires:  systemd

%description
Finger is a utility that allows users to see information about system users
(login name, home directory, name, and more) on local and remote systems.

%package server
Summary:                A Server for Showing User Information
Group:                  System Environment/Daemons
Requires:               finger
Requires:               systemd
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

%description server
The finger daemon implements a simple protocol based on RFC1196 that provides an
interface to the Name and Finger programs at several network sites. The program
is supposed to return a friendly human-oriented status report on either the
system at the moment or a person.

%prep
%autosetup -p1 -n  bsd-finger-%{version}

%build
sed -i 's/install -s/install/' finger/Makefile
sed -i 's/install -s/install/' fingerd/Makefile
if [ %{_host} != %{_build} ]; then
sed -i '/\.\/__conftest/d' configure
fi
sh configure --prefix=%{_prefix} --with-c-compiler=%{_host}-gcc

make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE3} LICENSE
make INSTALLROOT=%{buildroot} MANDIR=/usr/share/man install %{_smp_mflags}

%check
make -k check %{_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post server
%systemd_post finger.socket

%preun server
%systemd_preun finger.socket

%postun server
%systemd_postun_with_restart finger.socket

%files
%license LICENSE
%attr(0755,root,root) %{_bindir}/finger
%{_mandir}/man1/finger.1*

%files server
%license LICENSE
%{_unitdir}/finger.socket
%{_unitdir}/finger@.service
%attr(0755,root,root) %{_sbindir}/in.fingerd
%{_mandir}/man8/in.fingerd.8*
%{_mandir}/man8/fingerd.8*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.17-4
- Release bump for SRP compliance
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 0.17-3
- Cross compilation support
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.17-2
- Apply patch to generate debuginfo
* Wed Dec 7 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.17-1
- initial version
