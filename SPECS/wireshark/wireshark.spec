Summary:        Wireshark is the world's foremost protocol analyzer
Name:           wireshark
Version:        3.6.19
Release:        1%{?dist}
License:        GPL+
URL:            http://www.wireshark.org/
Source0:        https://wireshark.org/download/src/%{name}-%{version}.tar.xz
%define sha512 %{name}=cfa7e41c054e8610497501c36feac720cc9e5786c78ab6bab324d23d0059625e2cbdae70862eed468987e1f558ecb150eaec19185967703d4bdd334db8d9d77a
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

Patch0:        disable-glib-compact-g_memdup2.patch

BuildRequires:  bzip2-devel
BuildRequires:  c-ares-devel
BuildRequires:  elfutils-devel
BuildRequires:  gcc
BuildRequires:  glib-devel >= 2.58.3
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
BuildRequires:  python3-devel

Requires:       libpcap
Requires:       libnl
Requires:       pcre
Requires:       c-ares
Requires:       libcap
Requires:       libnl
Requires:       gnutls
Requires:       glib >= 2.58.3

%description
Wireshark is a network protocol analyzer. It allows examining data
from a live network or from a capture file on disk. You can
interactively browse the capture data, viewing summary and detailed
information for each packet. Wireshark has several features,
including a rich display filter language and the ability to view the
reconstructed stream of a TCP session.

%package devel
Summary:Development headers and libraries for wireshark
Requires: wireshark = %{version}-%{release} glibc-devel glib-devel

%description devel
The wireshark-devel package contains the header files, developer
documentation, and libraries required for development of wireshark scripts
and plugins.

%global debug_package %{nil}

%prep
%autosetup -p1

%build
%cmake -G "Ninja" \
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
        %{nil}

%ninja_build

%install
%ninja_install

rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_docdir}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/wireshark/*

%files devel
%doc doc/README.* ChangeLog
%{_includedir}/wireshark
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Nov 24 2023 Susant Sahani <ssahani@vmware.com> 3.6.19-1
- Update version and fix CVE-2023-6175
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.6.18-2
- Version bump due to glib change
* Tue Oct 10 2023 Susant Sahani <ssahani@vmware.com> 3.6.18-1
- Update version and fix CVE-2023-5371
* Mon Sep 11 2023 Harinadh D <hdommaraju@vmware.com> 3.6.16-2
- version bump to use updated c-ares
* Mon Aug 28 2023 Susant Sahani <ssahani@vmware.com> 3.6.16-1
- Update version and fix CVE-2023-4513
* Thu Jul 27 2023 Susant Sahani <ssahani@vmware.com> 3.6.15-1
- Update version and fix CVE-2023-0667, CVE-2023-3648
* Wed Jun 07 2023 Susant Sahani <ssahani@vmware.com> 3.6.14-1
- Update version and fix CVE-2023-2952
* Tue Apr 18 2023 Susant Sahani <ssahani@vmware.com> 3.6.13-1
- Update version and fix CVE-2023-1994
* Tue Mar 14 2023 Anmol Jain <anmolja@vmware.com> 3.6.11-2
- Version bump up to use c-ares
* Mon Jan 23 2023 Susant Sahani <ssahani@vmware.com> 3.6.11-1
- Update version and fix CVE
* Mon Nov 21 2022 Nitesh Kumar <ssahani@vmware.com> 3.6.9-1
- Version upgrade to address CVE-2022-3725
* Wed Oct 12 2022 Susant Sahani <ssahani@vmware.com> 3.6.8-1
- Update version and fix CVE
* Fri Feb 25 2022 Susant Sahani <ssahani@vmware.com> 3.6.2-1
- Update version and fix CVE
* Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 3.6.1-2
- Version Bump to build with new version of cmake
* Thu Jan 13 2022 Susant Sahani <ssahani@vmware.com> 3.6.1-1
- Update version and fix CVE-2021-4185
* Mon Dec 06 2021 Susant Sahani <ssahani@vmware.com> 3.6.0-1
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
