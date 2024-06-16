Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.20.1
Release:        12%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/rpm-software-management/createrepo_c

Source0: https://github.com/rpm-software-management/createrepo_c/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=54a2cc7c7cd3f3b9a0c23cd8c136ae1331e7fa7cc995189088e7e6f2276c78b2b84e21c2a2b93f4528b5e9e4018dd6525262c8aaba3bc8a1412a51dfafd101f7

BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  file-devel
BuildRequires:  glib-devel
BuildRequires:  libffi-devel
BuildRequires:  libxml2-devel
BuildRequires:  rpm-devel
BuildRequires:  xz-devel
BuildRequires:  sqlite-devel
BuildRequires:  python3-devel
BuildRequires:  drpm-devel
BuildRequires:  zchunk-devel
BuildRequires:  rpm-devel
BuildRequires:  zlib-devel

Requires:       zlib
Requires:       drpm
Requires:       zchunk-libs
Requires:       rpm-libs
Requires:       curl-libs
Requires:       openssl-libs
Requires:       xz-libs
Requires:       file-libs
Requires:       sqlite-libs
Requires:       zchunk-libs
Requires:       bzip2-libs
Requires:       glib
Requires:       popt
Requires:       libxml2

Obsoletes:      createrepo

Provides:       createrepo
Provides:       /bin/mergerepo
Provides:       /bin/modifyrepo

%description
C implementation of the createrepo.

%package devel
Summary:    Library for repodata manipulation
Requires:   %{name} = %{version}-%{release}
Requires:   glib-devel
Requires:   sqlite-devel
Requires:   libxml2-devel

Provides:   createrepo-devel

%description devel
headers and libraries for createrepo_c

%prep
%autosetup -p1

%build
%{cmake} \
    -DWITH_LIBMODULEMD=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo

%{cmake_build}

%install
%{cmake_install}
pushd %{buildroot}%{_bindir}
for b in createrepo mergerepo modifyrepo; do
  test -e ${b}_c && ln -srv ${b}_c ${b} || exit 1
done
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/*
%exclude %{_libdir}/python*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sun Jun 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.20.1-12
- Bump version as a part of rpm upgrade
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 0.20.1-11
- Bump version as a part of libxml2 upgrade
* Mon Mar 04 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 0.20.1-10
- Bump version as a part of sqlite upgrade to v3.43.2
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 0.20.1-9
- Bump version as a part of libxml2 upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.20.1-8
- Bump version as a part of openssl upgrade
* Thu Nov 09 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.20.1-7
- Bump version as a part of rpm upgrade
* Mon Sep 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.20.1-6
- Fix devel package requires
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.20.1-5
- Bump version as a part of libxml2 upgrade
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 0.20.1-4
- bump release as part of sqlite update
* Fri Jan 06 2023 Oliver Kurth <okurth@vmware.com> 0.20.1-3
- bump version as a part of xz upgrade
- add bzip2-devel to build requires
- relative symlinks
* Tue Jan 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.20.1-2
- Bump version as a part of rpm upgrade
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.20.1-1
- Upgrade to v0.20.1
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-7
- Bump version as a part of sqlite upgrade
* Thu Jul 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-6
- Bump version as a part of rpm upgrade
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-5
- Use cmake macros for build and install
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 0.16.0-4
- Release bump up to use libxml2 2.9.12-1.
* Tue Nov 16 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.16.0-3
- Bump up release for openssl
* Fri Aug 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-2
- Bump version as a part of rpm upgrade
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.16.0-1
- Automatic Version Bump
* Wed Jun 19 2019 Ankit Jain <ankitja@vmware.com> 0.11.1-2
- Added libxml2 as Requires for makecheck.
* Tue Sep 04 2018 Keerthana K <keerthanak@vmware.com> 0.11.1-1
- Updated to version 0.11.1.
* Mon Jun 04 2018 Xiaolin Li <xiaolinl@vmware.com> 0.10.0-2
- Provides modifyrepo and merge repo
* Wed Oct 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.10.0-1
- Initial
