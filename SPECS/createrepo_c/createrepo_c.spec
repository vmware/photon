Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.20.1
Release:        3%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/rpm-software-management/createrepo_c

Source0:        https://github.com/rpm-software-management/createrepo_c/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=54a2cc7c7cd3f3b9a0c23cd8c136ae1331e7fa7cc995189088e7e6f2276c78b2b84e21c2a2b93f4528b5e9e4018dd6525262c8aaba3bc8a1412a51dfafd101f7

BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  expat-devel
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

Requires:       drpm
Requires:       zchunk-libs
%if 0%{?with_check}
Requires:       libxml2
%endif

Obsoletes:      createrepo

Provides:       createrepo
Provides:       /bin/mergerepo
Provides:       /bin/modifyrepo

%description
C implementation of the createrepo.

%package devel
Summary:    Library for repodata manipulation
Requires:   %{name} = %{version}-%{release}

%description devel
headers and libraries for createrepo_c

%prep
%autosetup -p1
sed -e '/find_package(GTHREAD2/ s/^#*/#/' -i CMakeLists.txt
sed -i 's|g_thread_init|//g_thread_init|'  src/createrepo_c.c
sed -i 's|g_thread_init|//g_thread_init|'  src/mergerepo_c.c
sed -i 's|g_thread_init|//g_thread_init|'  src/modifyrepo_c.c
sed -i 's|g_thread_init|//g_thread_init|'  src/sqliterepo_c.c

%build
%cmake \
    -DWITH_LIBMODULEMD=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install
ln -sfv createrepo_c %{buildroot}%{_bindir}/createrepo
ln -sfv mergerepo_c %{buildroot}%{_bindir}/mergerepo
ln -sfv modifyrepo_c %{buildroot}%{_bindir}/modifyrepo

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
