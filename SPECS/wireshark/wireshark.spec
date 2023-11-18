Summary:        Wireshark is the world's foremost protocol analyzer
Name:           wireshark
Version:        4.0.8
Release:        2%{?dist}
License:        GPL+
URL:            http://www.wireshark.org
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://wireshark.org/download/src/%{name}-%{version}.tar.xz
%define sha512  %{name}=f6de0f86bb1eac82f7ed2d98d7f4fe3189107b1f0da441abd9077593f8e624989c33aaf8b4ef4b3c460fe787c64c4b8fdb3168de9f5661802fed6b06d71c5c65

BuildRequires:  bzip2-devel
BuildRequires:  c-ares-devel
BuildRequires:  elfutils-devel
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  gnutls-devel
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libnl-devel
BuildRequires:  libpcap-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  systemd-devel
BuildRequires:  git

Requires:       libpcap
Requires:       libnl
Requires:       pcre
Requires:       c-ares
Requires:       libcap
Requires:       libnl
Requires:       gnutls
Requires:       glib

%description
Wireshark is a network protocol analyzer. It allows examining data
from a live network or from a capture file on disk. You can
interactively browse the capture data, viewing summary and detailed
information for each packet. Wireshark has several features,
including a rich display filter language and the ability to view the
reconstructed stream of a TCP session.

%package        devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       glibc-devel
Requires:       glib-devel

%description    devel
The %{name}-devel package contains the header files, developer
documentation, and libraries required for development of %{name} scripts
and plugins.

%global debug_package %{nil}

%prep
%autosetup -p1

%build
%cmake -G "Unix Makefiles" \
       -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DDISABLE_WERROR=ON \
       -DENABLE_LUA=OFF \
       -DBUILD_mmdbresolve=OFF \
       -DBUILD_wireshark=OFF \
       -DBUILD_randpktdump=OFF \
       -DENABLE_SMI=ON \
       -DENABLE_PLUGINS=ON \
       -DENABLE_NETLINK=ON \
       -DBUILD_dcerpcidl2wrs=OFF \
       -DBUILD_sdjournal=ON \
       -DBUILD_sharkd=off \
       -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
       -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install

rm -rf %{buildroot}%{_mandir} \
       %{buildroot}%{_docdir}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/%{name}/*
%{_datadir}/%{name}/*

%files devel
%doc doc/README.* ChangeLog
%{_includedir}/%{name}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.0.8-2
- Bump version as a part of openssl upgrade
* Mon Aug 28 2023 Susant Sahani <ssahani@vmware.com> 4.0.8-1
- Update version and fix CVE-2023-4513
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.0.6-2
- Bump version as a part of elfutils upgrade
* Tue Jun 06 2023 Susant Sahani <ssahani@vmware.com> 4.0.6-1
- Update version and fix CVE-2023-2953
* Tue Apr 18 2023 Susant Sahani <ssahani@vmware.com> 4.0.5-1
- Update version and fix CVE
* Mon Jan 23 2023 Susant Sahani <ssahani@vmware.com> 4.0.3-1
- Update version
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.0.2-2
- Bump up due to change in elfutils
* Sat Dec 10 2022 Susant Sahani <ssahani@vmware.com> 4.0.2-1
- Update version
* Tue Nov 1 2022 Gerrit Photon <photon-checkins@vmware.com> 4.0.1-1
- Automatic Version Bump
* Wed Oct 12 2022 Susant Sahani <ssahani@vmware.com> 4.0.0-1
- Update version
* Tue Sep 20 2022 Susant Sahani <ssahani@vmware.com> 3.6.8-1
- Update version and fix CVE
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.6.2-3
- Bump version as a part of gnutls upgrade
* Tue Jun 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.6.2-2
- Spec fixes to make it work with latest cmake
* Fri Feb 25 2022 Susant Sahani <ssahani@vmware.com> 3.6.2-1
- Update version and fix CVE
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 3.6.1-1
- Update version and fix CVE-2021-4185
* Tue Nov 30 2021 Susant Sahani <ssahani@vmware.com> 3.6.0-1
- Update version and fix CVE-2021-39922, CVE-2021-39923, CVE-2021-39929
- CVE-2021-39924, CVE-2021-39925, CVE-2021-39926, CVE-2021-39922,
- CVE-2021-39921, CVE-2021-39920, CVE-2021-39928
* Tue Aug 03 2021 Susant Sahani <ssahani@vmware.com> 3.4.7-1
- Update version and fix CVE-2021-22235
* Tue Jun 29 2021 Susant Sahani <ssahani@vmware.com> 3.4.6-1
- Update version and fix CVE-2021-22222
* Tue May 11 2021 Susant Sahani <ssahani@vmware.com> 3.4.5-1
- Update version and fix CVE-2021-22207
* Tue Mar 16 2021 Susant Sahani <ssahani@vmware.com> 3.4.4-1
- Update version and fix CVE-2021-22174
* Mon Jan 25 2021 Susant Sahani <ssahani@vmware.com> 3.4.2-1
- Initial rpm release
