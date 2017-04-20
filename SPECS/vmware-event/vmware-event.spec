Name:          vmware-event
Summary:       VMware Event SDK
Version:       1.2.0
Release:       1%{?dist}
License:       Apache 2.0
Group:         Applications/System
Vendor:        VMware, Inc.
URL: 	       https://github.com/vmware/lightwave
Source0:       lightwave-%{version}.tar.gz
%define sha1 lightwave=223d98f15b67f531fc8eeed824756cb313a2ac01
Distribution:  Photon
Requires:       coreutils >= 8.22
BuildRequires:  coreutils >= 8.22

%description
VMware Event Service Software Development Kit

%package    devel
Summary:    Header files for VMWare Event Service
Group:      Development/Libraries

%description devel
VMware Event Service Software Development Kit

%prep
%setup -qn lightwave-%{version}

%define _prefix /opt/vmware
%define _includedir %{_prefix}/include

%build
cd vmevent/build
autoreconf -mif ..
../configure \
    --prefix=%{_prefix}

make

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd vmevent/build && make install DESTDIR=$RPM_BUILD_ROOT

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
*   Thu Mar 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   Initial - spec modified for Photon from lightwave git repo.
