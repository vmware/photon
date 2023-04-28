Summary:        NETCONF library in C intended for building NETCONF clients and servers.
Name:           libnetconf2
Version:        2.1.18
Release:        2%{?dist}
License:        BSD-3-Clause
Group:          Development/Tools
URL:            https://github.com/CESNET/libnetconf2
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/CESNET/libnetconf2/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=01ca262c3e530f3d89e61838f08bf3abeae5c9c3c1cf9570416183a2060b850c18bdf661154ec31f7b57b13067c956fe01453ebc461d0d3935e841073a39fb20

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libssh-devel
BuildRequires:  openssl-devel
BuildRequires:  libyang-devel
BuildRequires:  pcre2-devel
BuildRequires:  Linux-PAM-devel

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
%dir %{_includedir}/%{name}

%changelog
* Tue Apr 11 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.1.18-2
- Bump version as part of libyang upgrade
* Mon Oct 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.18-1
- Automatic Version Bump
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.1.7-3
- Bump version as a part of libyang upgrade
- Fix file packaging and spec issues
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.1.7-2
- Fix cmocka dependency
* Thu Mar 24 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 2.1.7-1
- Initial addition to Photon. Modified from provided libnetconf2 GitHub repo version.
