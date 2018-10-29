Summary:	Data for network services and protocols
Name:		iana-etc
Version:	2.30
Release:	2%{?dist}
License:	OSLv3
URL:		http://freshmeat.net/projects/iana-etc
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:	noarch
Source0:	http://anduin.linuxfromscratch.org/sources/LFS/lfs-packages/conglomeration//iana-etc/%{name}-%{version}.tar.bz2
%define sha1 iana-etc=218593bcb9264014c4e397d838b2c218eac9df06
%description
The Iana-Etc package provides data for network services and protocols.
%prep
%setup -q
%build
if [ %{_host} != %{_build} -a %{_target} = "i686-linux" ]; then
export CC=i686-linux-gnu-gcc
export CXX=i686-linux-gnu-g++
export AR=i686-linux-gnu-ar
export AS=i686-linux-gnu-as
export RANLIB=i686-linux-gnu-ranlib
export LD=i686-linux-gnu-ld
export STRIP=i686-linux-gnu-strip
fi
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%config %_sysconfdir/protocols
%config %_sysconfdir/services
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.30-2
-	GA - Bump release of all rpms
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.30-1
-	Initial build.	First version
