Summary:       A Metalink library written in C language
Name:          libmetalink
Version:       0.1.3
Release:       3%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
License:       MIT
URL:           https://launchpad.net/%{name}
Source0:       %{url}/trunk/%{name}-%{version}/+download/%{name}-%{version}.tar.bz2
%define sha1 %{name}-%{version}=20ccbea4b495d60ab6d9dd3e40b3a429cfa2584b
Distribution:  Photon

Requires:      expat
Requires:      glibc

BuildRequires: expat-devel
BuildRequires: glibc
BuildRequires: glibc-devel

%description
A Metalink library written in C language.

%package devel
Summary:    Development files for libmetalink
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for libmetalink

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
install -Dm644 COPYING %{buildroot}%{_defaultlicensedir}/%{name}-%{version}/LICENSE

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
%{_defaultlicensedir}/*
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/*

%changelog
*  Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.1.3-3
-  Fix build with new rpm
*  Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 0.1.3-2
-  Used configure macro
*  Thu Jun 04 2020 Tapas Kundu <tkundu@vmware.com> 0.1.3-1
-  Initial packaging in Photon.
