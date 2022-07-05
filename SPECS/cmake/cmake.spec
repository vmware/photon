%global major_version 3
%define rpm_macros_dir %{_libdir}/rpm/macros.d

Summary:    Cmake
Name:       cmake
Version:    3.23.2
Release:    1%{?dist}
License:    BSD and LGPLv2+
URL:        http://www.cmake.org
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/Kitware/CMake/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=0925adf973d642fd76d4089b61b3882babb0a85050c4c57d5f5f3bd6b17564a9feb0beed236cd636e25f69072fa30b67ea3f80932380b6b6576f2dd78b8e6931

Source1:    macros.cmake

BuildRequires:  ncurses-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  curl
BuildRequires:  curl-devel
BuildRequires:  expat-libs
BuildRequires:  expat-devel
BuildRequires:  zlib
BuildRequires:  zlib-devel
BuildRequires:  libarchive
BuildRequires:  libarchive-devel
BuildRequires:  bzip2
BuildRequires:  bzip2-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  (toybox or coreutils)

Requires:       libgcrypt
Requires:       ncurses
Requires:       expat
Requires:       zlib
Requires:       libarchive
Requires:       bzip2

%description
CMake is an extensible, open-source system that manages the build process in an
operating system and in a compiler-independent manner.

%prep
%autosetup -p1

%build
./bootstrap --prefix=%{_prefix} \
            --system-expat \
            --system-zlib \
            --system-libarchive \
            --system-bzip2 \
            --parallel=$(nproc)

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
install -Dpm0644 %{SOURCE1} %{buildroot}%{rpm_macros_dir}/macros.%{name}
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{rpm_macros_dir}/macros.%{name}
touch -r %{SOURCE1} %{buildroot}%{rpm_macros_dir}/macros.%{name}

%if 0%{?with_check}
%check
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root)
%{_datadir}/%{name}-*/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/emacs/site-lisp/cmake-mode.el
%{_datadir}/vim/vimfiles/*
%{_bindir}/*
%{_usr}/doc/%{name}-*/*
%{_datadir}/aclocal/*
%{_libdir}/rpm/macros.d/macros.cmake

%changelog
* Tue Jun 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.23.2-1
- Upgrade to v3.23.2
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.18.3-4
- Bump up release for openssl
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.18.3-3
- Fix build with new rpm
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.18.3-2
- Bump for openssl 1.1.1 compatibility
* Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.18.3-1
- Automatic Version Bump
* Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 3.18.2-1
- Automatic Version Bump
* Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 3.18.1-1
- Automatic Version Bump
* Tue Jul 14 2020 Gerrit Photon <photon-checkins@vmware.com> 3.18.0-1
- Automatic Version Bump
* Mon Dec 16 2019 Sriram Nambakam <snambakam@vmware.com> 3.16.1-1
- Upgraded to 3.16.1
* Thu Jan 17 2019 Ankit Jain <ankitja@vmware.com> 3.12.1-4
- Removed unnecessary libgcc-devel buildrequires
* Thu Dec 06 2018 <ashwinh@vmware.com> 3.12.1-3
- Bug Fix 2243672. Add system provided libs.
* Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 3.12.1-2
- smp make (make -jN)
- specify /usr/lib as CMAKE_INSTALL_LIBDIR
* Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 3.12.1-1
- Upgrading version to 3.12.1
- Adding macros.cmake
* Fri Sep 29 2017 Kumar Kaushik <kaushikk@vmware.com> 3.8.0-4
- Building using system expat libs.
* Thu Aug 17 2017 Kumar Kaushik <kaushikk@vmware.com> 3.8.0-3
- Fixing make check bug # 1632102.
* Tue May 23 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.8.0-2
- bug 1448414: Updated to build in parallel
* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  3.8.0-1
- Upgrade to 3.8.0
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 3.4.3-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.3-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.4.3-1
- Updated version.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 3.2.1.2
- Updated group.
* Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-1
- Update to 3.2.1
* Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.2-1
- Initial build. First version
