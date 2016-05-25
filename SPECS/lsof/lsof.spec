Summary:	List Open Files
Name:		lsof
Version:	4.89
Release:	2%{?dist}
License:	BSD
URL:		https://people.freebsd.org/~abe/
Group:		System Environment/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://fossies.org/linux/misc/%{name}_%{version}.tar.gz
%define sha1 lsof=e2fee8dfae031b736660b029a4d9a808bc599c2f
BuildRequires:	libtirpc-devel
Requires:	libtirpc

%description
Contains programs for generating Makefiles for use with Autoconf.
%prep
%setup -q -n %{name}_%{version} 
tar -xf lsof_4.89_src.tar
%build
cd lsof_4.89_src
./Configure -n linux
make CFGL="-L./lib -ltirpc" %{?_smp_mflags}
%install
cd lsof_4.89_src
mkdir -p %{buildroot}%{_sbindir}
install -v -m 0755 lsof %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
install -v -m 0644 lsof.8 %{buildroot}%{_mandir}/man8
%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	4.89-2
-	GA - Bump release of all rpms
*	Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 4.89-1
-	Initial build.
