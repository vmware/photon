Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.16.0
Release:        10%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/rpm-software-management/createrepo_c

Source0: https://github.com/rpm-software-management/createrepo_c/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=78105c36bc75b5881ebafbec38a46063d46b9a8d7e26cd797bfd90af85534f1ef187d366b597b65798257e8236367507cec6487726b287d8d570a054fb31ba34

Patch0:         remove-distutils.patch

BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  file-devel
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  libffi-devel
BuildRequires:  libxml2-devel
BuildRequires:  rpm-devel
BuildRequires:  xz-devel
BuildRequires:  sqlite-devel
BuildRequires:  python3-devel
BuildRequires:  drpm-devel
BuildRequires:  zchunk-devel
BuildRequires:  doxygen

Requires:       drpm
Requires:       zchunk-libs
Requires:       glib
Requires:       sqlite

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
Requires:   glib-devel
Requires:   sqlite-devel
Requires:   libxml2-devel

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
ln -sf %{_bindir}/createrepo_c %{buildroot}%{_bindir}/createrepo
ln -sf %{_bindir}/mergerepo_c %{buildroot}%{_bindir}/mergerepo
ln -sf %{_bindir}/modifyrepo_c %{buildroot}%{_bindir}/modifyrepo

%clean
rm -rf %{buildroot}/*

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
* Tue Jan 07 2025 Tapas Kundu <tapas.kundu@broadcom.com> 0.16.0-10
- Release bump for SRP
* Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 0.16.0-9
- Bump version as a part of expat upgrade & Fix devel package requires
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.16.0-8
- Bump version as part of glib upgrade
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-7
- Use cmake macros
* Tue Jun 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-6
- Bump version as a part of sqlite upgrade
* Mon Nov 22 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.16.0-5
- Remove deprecated distutils to compile with python 3.10
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 0.16.0-4
- Release bump up to use libxml2 2.9.12-1.
* Fri Aug 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.16.0-3
- Bump version as a part of rpm upgrade
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.16.0-2
- Bump up release for openssl
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
