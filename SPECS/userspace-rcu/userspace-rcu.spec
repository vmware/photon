Summary:        user space RCU (read-copy-update)
Name:           userspace-rcu
Version:        0.13.2
Release:        4%{?dist}
URL:            https://github.com/urcu/userspace-rcu/releases
Source0:         %{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libxml2-devel
BuildRequires:  nss-devel
BuildRequires:  m4
BuildRequires:  elfutils-devel
BuildRequires:  popt-devel

%description
This data synchronization library provides read-side access which scales linearly with the number of cores.

%package devel
Summary: Development Libraries for openssl
Group: Development/Libraries
Requires: userspace-rcu = %{version}-%{release}
%description devel
Library files for doing development with userspace-rcu.

%prep
%autosetup

%build
autoreconf -fiv
%configure \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%files
%{_lib}/*.so.*
%{_includedir}/*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.13.2-4
- Release bump for SRP compliance
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.13.2-3
- Bump version as a part of libxml2 upgrade
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.13.2-2
- Bump up due to change in elfutils
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.13.2-1
- Automatic Version Bump
* Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 0.13.1-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.12.1-1
- Automatic Version Bump
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 0.10.1-1
- Updated to version 0.10.1.
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 0.9.3-1
- Updated to version 0.9.3.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.9.1-4
- Modified %check
* Mon Jul 25 2016 Divya Thaluru <dthaluru@vmware.com> 0.9.1-3
- Added devel package and removed packaging of debug files
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.1-2
- GA - Bump release of all rpms
* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
- Initial build.  First version
