Summary:        Wireshark is the world's foremost protocol analyzer
Name:           wireshark
Version:        3.4.4
Release:        1%{?dist}
License:        GPL+
URL:            http://www.wireshark.org/
Source0:        https://wireshark.org/download/src/%{name}-%{version}.tar.xz
%define sha1 wireshark=fa5c553596dcc6a59735f96a9a0845e3c40abab2
Group:          Networking
Vendor:         VMware, Inc.
Distribution:   Photon

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
%cmake -G "Unix Makefiles" \
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
       -DBUILD_=OFF \
       -G Ninja

%ninja_build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
DESTDIR=%{buildroot} ninja install

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
*   Tue Mar 16 2021 Susant Sahani <ssahani@vmware.com> 3.4.4-1
-   Update version and fix CVE-2021-22174
*   Mon Jan 25 2021 Susant Sahani <ssahani@vmware.com> 3.4.2-1
-   Initial rpm release
