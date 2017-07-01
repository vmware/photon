Summary: user space RCU (read-copy-update)
Name:    userspace-rcu
Version: 0.9.1
Release: 3%{?dist}
License: LGPLv2+
URL: http://liburcu.org
Source: %{name}-%{version}.tar.bz2
%define sha1 userspace-rcu=ca1b603655c3c5bf5d5b6254117999e3ae5f6751
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires: libxml2-devel
BuildRequires: nss-devel
BuildRequires: m4
BuildRequires: elfutils-devel
BuildRequires: popt-devel

%description
This data synchronization library provides read-side access which scales linearly with the number of cores.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
%{buildroot} -name '*.la' -delete

%files
%{_lib}/*.so*
%{_lib}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/*


%changelog
*   Fri Jun 30 2017 Divya Thaluru <dthaluru@vmware.com> 0.9.1-3
-   Removed packaging of debug files
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.1-2
-   GA - Bump release of all rpms
*   Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build.  First version
