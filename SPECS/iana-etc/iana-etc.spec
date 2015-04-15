Summary:	Data for network services and protocols
Name:		iana-etc
Version:	2.30
Release:	1
License:	OSLv3
URL:		http://freshmeat.net/projects/iana-etc
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:	noarch
Source0:	http://anduin.linuxfromscratch.org/sources/LFS/lfs-packages/conglomeration//iana-etc/%{name}-%{version}.tar.bz2
%description
The Iana-Etc package provides data for network services and protocols.
%prep
%setup -q
%build
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
%config %_sysconfdir/protocols
%config %_sysconfdir/services
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.30-1
-	Initial build.	First version
