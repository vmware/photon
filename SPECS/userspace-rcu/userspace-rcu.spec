Summary:        user space RCU (read-copy-update)
Name:           userspace-rcu
Version:        0.13.2
Release:        9%{?dist}
License:        LGPLv2+
URL:            https://github.com/urcu/userspace-rcu/releases
Source:         %{name}-%{version}.tar.gz
%define sha512  userspace-rcu=a59daf9908acad3bd21e36d90c831ec2df8259d29743fb86066a82433a4a228ae79ca3b66e12120c0e6cad651a1007e77d6ac23ab083c55ab9b283b7d36a3ddc
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

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
* Tue Aug 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.13.2-9
- Bump version as a part of nss upgrade
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 0.13.2-8
- Bump version as a part of libxml2 upgrade
* Thu Mar 14 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.13.2-7
- Bump version as a part of nss upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 0.13.2-6
- Bump version as a part of libxml2 upgrade
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.13.2-5
- Bump version as a part of elfutils upgrade
* Tue May 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.13.2-4
- Bump version as a part of nss upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.13.2-3
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
