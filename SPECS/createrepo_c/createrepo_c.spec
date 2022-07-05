Summary:        Creates a common metadata repository
Name:           createrepo_c
Version:        0.16.0
Release:        4%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/rpm-software-management/createrepo_c

Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=78105c36bc75b5881ebafbec38a46063d46b9a8d7e26cd797bfd90af85534f1ef187d366b597b65798257e8236367507cec6487726b287d8d570a054fb31ba34

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
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DWITH_LIBMODULEMD=OFF ..
%make_build

%install
cd build
%make_install %{?_smp_mflags}
ln -sfv %{_bindir}/createrepo_c %{buildroot}%{_bindir}/createrepo
ln -sfv %{_bindir}/mergerepo_c %{buildroot}%{_bindir}/mergerepo
ln -sfv %{_bindir}/modifyrepo_c %{buildroot}%{_bindir}/modifyrepo

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/*
%{_lib64dir}/*.so.*
%{_mandir}/*
%exclude %{_libdir}/python*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_lib64dir}/*.so
%{_lib64dir}/pkgconfig/%{name}.pc

%changelog
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
