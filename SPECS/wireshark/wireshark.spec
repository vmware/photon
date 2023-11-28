Summary:        Wireshark is the world's foremost protocol analyzer
Name:           wireshark
Version:        4.0.11
Release:        2%{?dist}
License:        GPL+
URL:            http://www.wireshark.org
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://wireshark.org/download/src/%{name}-%{version}.tar.xz
%define sha512 %{name}=c027b279f9bc761c5c701131df9e57d3f2568129f63c919cd744f6626843eb0e000caebc3e01c9a10eedad35874c01c880d2c736b62f8e841da35c375a37c53f

BuildRequires:  bzip2-devel
BuildRequires:  c-ares-devel
BuildRequires:  elfutils-devel
BuildRequires:  gcc
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  gnutls-devel
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libnl-devel
BuildRequires:  libpcap-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  systemd-devel
BuildRequires:  git
BuildRequires:  python3-devel

Requires:       libpcap
Requires:       libnl
Requires:       pcre2
Requires:       c-ares
Requires:       libcap
Requires:       libnl
Requires:       gnutls
Requires:       glib >= 2.68.4

%description
Wireshark is a network protocol analyzer. It allows examining data
from a live network or from a capture file on disk. You can
interactively browse the capture data, viewing summary and detailed
information for each packet. Wireshark has several features,
including a rich display filter language and the ability to view the
reconstructed stream of a TCP session.

%package devel
Summary:    Development headers and libraries for wireshark
Requires:   %{name} = %{version}-%{release} glibc-devel glib-devel

%description devel
The wireshark-devel package contains the header files, developer
documentation, and libraries required for development of wireshark scripts
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
       -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
       -DBUILD_sharkd=off \
       -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install

rm -rf %{buildroot}%{_mandir} \
       %{buildroot}%{_docdir}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/wireshark/*

%files devel
%defattr(-,root,root)
%doc doc/README.* ChangeLog
%{_includedir}/wireshark
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Nov 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.0.11-2
- Bump version as a part of gnutls upgrade
* Tue Nov 21 2023 Susant Sahani <ssahani@vmware.com> 4.0.11-1
- Update version and fix CVE-2023-6174
* Wed Oct 11 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.0.10-2
- Bump version as part of glib upgrade
* Tue Oct 10 2023 Susant Sahani <ssahani@vmware.com> 4.0.10-1
- Update version and fix CVE-2023-5371
* Mon Aug 28 2023 Susant Sahani <ssahani@vmware.com> 4.0.8-1
- Update version and fix CVE-2023-4513
* Mon Jul 17 2023 Susant Sahani <ssahani@vmware.com> 4.0.7-1
- Update version and fix CVE-2023-3649, CVE-2023-2952
- CVE-2023-0666, CVE-2023-3648
* Tue Jun 06 2023 Susant Sahani <ssahani@vmware.com> 4.0.6-1
- Update version and fix CVE-2023-2953
* Tue Apr 18 2023 Susant Sahani <ssahani@vmware.com> 4.0.5-1
- Update version and fix CVE-2023-1994
* Wed Mar 15 2023 Anmol Jain <anmolja@vmware.com> 4.0.3-2
- Version bump up to use c-ares
* Mon Jan 23 2023 Susant Sahani <ssahani@vmware.com> 4.0.3-1
- Update version and fix CVE
* Mon Nov 21 2022 Nitesh Kumar <ssahani@vmware.com> 3.6.9-1
- Version upgrade to address CVE-2022-3725
* Tue Sep 20 2022 Susant Sahani <ssahani@vmware.com> 3.6.8-1
- Update version and fix CVE
* Fri Feb 25 2022 Susant Sahani <ssahani@vmware.com> 3.6.2-1
- Update version and fix CVE
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 3.6.1-1
- Update version and fix CVE-2021-4185
* Tue Nov 30 2021 Susant Sahani <ssahani@vmware.com> 3.6.0-1
- Update version and fix CVE-2021-39922, CVE-2021-39923, CVE-2021-3992
- CVE-2021-39924, CVE-2021-39925, CVE-2021-39926, CVE-2021-39922,
- CVE-2021-39921, CVE-2021-39920, CVE-2021-39928
* Tue Aug 03 2021 Susant Sahani <ssahani@vmware.com> 3.4.7-1
- Update version and fix CVE-2021-22235
* Tue Jun 29 2021 Susant Sahani <ssahani@vmware.com> 3.4.6-1
- Update version and fix CVE-2021-22222
* Tue May 11 2021 Susant Sahani <ssahani@vmware.com> 3.4.5-1
- Update version and fix CVE-2021-22207
* Tue Mar 16 2021 Susant Sahani <ssahani@vmware.com> 3.4.4-1
- Update version and fix CVE-2021-22174 CVE-2021-22173
* Mon Jan 25 2021 Susant Sahani <ssahani@vmware.com> 3.4.2-1
- Initial rpm release
