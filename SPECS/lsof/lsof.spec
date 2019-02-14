Summary:	List Open Files
Name:		lsof
Version:	4.91
Release:	1%{?dist}
License:	BSD
URL:		https://people.freebsd.org/~abe/
Group:		System Environment/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://fossies.org/linux/misc/%{name}_%{version}.tar.bz2
%define sha1 lsof=da6f9883d00f200671f6e47cf838bb9b6b9c6f01
BuildRequires:	libtirpc-devel
Requires:	libtirpc

%description
Contains programs for generating Makefiles for use with Autoconf.

%prep
%setup -q -n %{name}_%{version} 
tar -xf %{name}_%{version}_src.tar

%build
cd %{name}_%{version}_src
./Configure -n linux
make CFGL="-L./lib -ltirpc" %{?_smp_mflags}

%install
cd %{name}_%{version}_src
mkdir -p %{buildroot}%{_sbindir}
install -v -m 0755 lsof %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
install -v -m 0644 lsof.8 %{buildroot}%{_mandir}/man8

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
*       Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.91-1
-       Update to version 4.91
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.89-2
-	GA - Bump release of all rpms
*	Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 4.89-1
-	Initial build.
