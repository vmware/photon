%global major_version 3

Summary:      Cross-platform make system
Name:         cmake
Version:      3.25.2
Release:      6%{?dist}
URL:          http://www.cmake.org
Group:        Development/Tools
Vendor:       VMware, Inc.
Distribution: Photon

Source0: https://github.com/Kitware/CMake/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=20146d06a1722c36249192944a58e4780aad334d2bc5ce2a3d8c4f24656630c5b71ca0ae7ed53587e3d46f488bd773452fa60c3fc7045fe54db2dbc6ffd86390

Source1: macros.cmake
Source2: license.txt
%include %{SOURCE2}

BuildRequires: ncurses-devel
BuildRequires: xz-devel
BuildRequires: curl-devel
BuildRequires: expat-devel
BuildRequires: zlib-devel
BuildRequires: libarchive-devel
BuildRequires: bzip2-devel
BuildRequires: libgcrypt-devel
BuildRequires: coreutils >= 9.1-7

Requires: libgcrypt
Requires: ncurses
Requires: expat
Requires: zlib
Requires: libarchive
Requires: bzip2
Requires: curl-libs

%description
CMake is an extensible, open-source system that manages the build process in an
operating system and in a compiler-independent manner.

%prep
%autosetup -p1

%build
./bootstrap --prefix=%{_prefix} \
            --system-expat \
            --system-zlib \
            --system-curl \
            --system-libarchive \
            --system-bzip2 \
            --parallel=$(nproc)

%make_build

%install
%make_install %{?_smp_mflags}
install -Dpm0644 %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.%{name}
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{_rpmmacrodir}/macros.%{name}
touch -r %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.%{name}

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
%{_rpmmacrodir}/macros.%{name}

%changelog
* Tue Dec 10 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.25.2-6
- Require coreutils only
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.25.2-5
- Release bump for SRP compliance
* Fri Jun 16 2023 Anmol Jain <anmolja@vmware.com> 3.25.2-4
- Use system curl
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 3.25.2-3
- Bump version as a part of ncurses upgrade to v6.4
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.25.2-2
- Bump version as a part of zlib upgrade
* Thu Feb 16 2023 Gerrit Photon <photon-checkins@vmware.com> 3.25.2-1
- Automatic Version Bump
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.25.1-3
- Fix requires
* Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 3.25.1-2
- bump version as a part of xz upgrade
* Thu Dec 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.25.1-1
- Upgrade to v3.25.1
* Wed Sep 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.24.1-1
- Upgrade to v3.24.1
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
