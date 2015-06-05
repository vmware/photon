Summary:	Utilities for configuring and managing bridge devices
Name:		bridge-utils
Version:	1.5
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://sourceforge.net/projects/bridge/files/bridge/%{name}-%{version}.tar.gz
Patch0:		http://www.linuxfromscratch.org/patches/blfs/systemd/bridge-utils-1.5-linux_3.8_fix-1.patch
%description
The bridge-utils package contains a utility needed to create and manage bridge devices. This is useful in setting up networks for a hosted virtual machine (VM).
%prep
%setup -q
%patch0 -p1
%build
autoconf -o configure configure.in 
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
%{_sbindir}/brctl
%{_mandir}/man8/*

%changelog
*	Tue May 19 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
-	Initial build.	First version
