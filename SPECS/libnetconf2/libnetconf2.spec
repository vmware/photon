Summary:        NETCONF library in C intended for building NETCONF clients and servers.
Name:           libnetconf2
Version:        3.5.5
Release:        1%{?dist}
License:        BSD-3-Clause
Group:          Development/Tools
URL:            https://github.com/CESNET/libnetconf2
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/CESNET/libnetconf2/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=8de6ef5ca31581bdc17f3711175392bc328dbc7560dc491bbdf8d1742b390b01781e750ac40cff504b32a610b9eff978334bd0e0b02b0622439fed34af119398

BuildRequires: cmake
BuildRequires: make
BuildRequires: gcc
BuildRequires: curl-devel
BuildRequires: libssh-devel
BuildRequires: openssl-devel
BuildRequires: libyang-devel
BuildRequires: pcre2-devel
BuildRequires: Linux-PAM-devel

Requires: pcre2
Requires: libyang
Requires: libssh

%if 0%{?with_check}
BuildRequires:  cmocka-devel
%endif

%description
libnetconf2 is a NETCONF library in C intended for building NETCONF clients and
servers. NETCONF is the NETwork CONFiguration protocol introduced by IETF.

%package devel
Summary:    Development libraries for libnetconf2
Requires: %{name} = %{version}-%{release}
Requires:  libssh-devel
Requires:  openssl-devel
Requires:  libyang-devel

%description devel
Headers of libnetconf library.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DENABLE_TESTS=ON \
    -DENABLE_TLS=ON \
    -DENABLE_SSH=ON

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
echo $'\n[SAN]\nsubjectAltName=IP:127.0.0.1' >> /etc/ssl/openssl.cnf
pushd tests/data
openssl req \
    -out server.csr \
    -key server.key \
    -new \
    -days 1 \
    -subj "/C=CZ/ST=Some-State/L=Brno/OU=TMC/CN=127.0.0.1"
openssl x509 \
    -req -in server.csr \
    -CA serverca.pem \
    -CAkey serverca.key \
    -out server.crt \
    -days 1 \
    -sha256 \
    -extensions SAN \
    -extfile /etc/ssl/openssl.cnf
popd
%ctest
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/%{name}.so.*
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so
%{_includedir}/*.h
%{_includedir}/%{name}/*.h
%{_datadir}/yang/modules/%{name}/*.yang
%dir %{_includedir}/%{name}

%changelog
* Mon Mar 24 2025 Harinadh Dommraju <Harinadh.Dommaraju@broadcom.com> 3.5.5-1
- Version update
* Tue Dec 26 2023 Mukul Sikka <msikka@vmware.com> 2.1.18-3
- Version bump up to use libssh v0.10.5
* Tue Sep 05 2023 Nitesh Kumar <kunitesh@vmware.com> 2.1.18-2
- Version bump up to use libssh v0.10.5
* Mon Apr 17 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.1.18-1
- Initial addition to Photon 4.0. Modified from provided libnetconf2 GitHub repo version.
