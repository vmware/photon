Summary:        NETCONF library in C intended for building NETCONF clients and servers.
Name:           libnetconf2
Version:        2.1.7
Release:        1%{?dist}
License:        BSD-3-Clause
Group:          Development/Tools
URL:            https://github.com/CESNET/libnetconf2
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/CESNET/libnetconf2/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha1 %{name}=bac66d22bc7928f5fbd77850775f79f73e4b18b8

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libssh-devel
BuildRequires:  openssl-devel
BuildRequires:  libyang-devel
BuildRequires:  pcre2-devel

Requires: pcre2
Requires: libyang
Requires: libssh

%if 0%{?with_check}
BuildRequires:  cmocka
%endif

%description
libnetconf2 is a NETCONF library in C intended for building NETCONF clients and
servers. NETCONF is the NETwork CONFiguration protocol introduced by IETF.

%package devel
Summary: Development libraries for libnetconf2

%description devel
Headers of libnetconf library.

%prep
%autosetup -p1

%build
mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DCMAKE_BUILD_TYPE:String="Release" \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DENABLE_TESTS=ON \
    -DENABLE_TLS=ON \
    -DENABLE_SSH=ON \
    ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
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
cd build
ctest --output-on-failure
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/%{name}.so*
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*.h
%{_includedir}/%{name}/*.h
%dir %{_includedir}/%{name}

%changelog
*   Thu Mar 24 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 2.1.7-1
-   Initial addition to Photon. Modified from provided libnetconf2 GitHub repo version.