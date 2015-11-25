Summary: LTTng is an open source tracing framework for Linux.
Name:    lttng-tools
Version: 2.7.0
Release: 1%{?dist}
License: GPLv2 and LGPLv2
URL: https://lttng.org/download/
Source: %{name}-%{version}.tar.bz2
%define sha1 lttng-tools=c1f23688f13c7db0f65ba7edd070fdb41adec823
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires: libxml2-devel
BuildRequires: nss-devel
BuildRequires: m4
BuildRequires: elfutils-devel
BuildRequires: popt-devel
BuildRequires: userspace-rcu

%description
LTTng is an open source tracing framework for Linux.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--disable-static \
	--disable-lttng-ust

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%{_bindir}/*
%{_includedir}/*
%{_lib}/*
%{_datadir}/*

%changelog
*	Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build.  First version
