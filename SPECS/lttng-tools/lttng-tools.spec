Summary: LTTng is an open source tracing framework for Linux.
Name:    lttng-tools
Version: 2.7.1
Release: 2%{?dist}
License: GPLv2 and LGPLv2
URL: https://lttng.org/download/
Source: %{name}-%{version}.tar.bz2
%define sha1 lttng-tools=f0c24ddc0ef370b0194c2c6d3b0a2dc19348c8aa
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires: libxml2-devel
BuildRequires: nss-devel
BuildRequires: m4
BuildRequires: elfutils-devel
BuildRequires: popt-devel
BuildRequires: userspace-rcu
Requires:      userspace-rcu
Requires:      elfutils
Requires:      nss
Requires:      libxml2
%description
LTTng is an open source tracing framework for Linux.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--disable-lttng-ust

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%{_bindir}/*
%{_includedir}/*
%{_lib}/*
%{_datadir}/*
%exclude %{_libdir}/debug

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  2.7.1-2
-	GA - Bump release of all rpms
*   Thu Jan 28 2016 Xiaolin Li <xiaolinl@vmware.com> 2.7.1-1
-   Updated to version 2.7.1
*	Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build.  First version
