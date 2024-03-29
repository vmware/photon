Summary:	NSS module to read passwd/group files from alternate locations
Name:		nss-altfiles
Version:	2.23.0
Release:	1%{?dist}
License:	LGPL 2.1
URL:		https://github.com/aperezdc/nss-altfiles
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/aperezdc/nss-altfiles/archive/%{name}-%{version}.tar.gz
%define sha1 nss-altfiles=dec35095f974b6dbe460c770443c0e70cbeb1b56
BuildRequires: glibc-devel

%description
NSS module to read passwd/group files from alternate locations.

%prep
%setup -q

%build
env CFLAGS='%{optflags}' ./configure --prefix=%{_prefix} --libdir=%{_libdir}

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md
%{_libdir}/*.so.*

%changelog
*	Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.23.0-1
-	Update to 2.23.0
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.19.1-2
-	GA - Bump release of all rpms
*   Sat Jul 11 2015 Touseef Liaqat <tliaqat@vmware.com> 2.19.1-2
-   Initial version
