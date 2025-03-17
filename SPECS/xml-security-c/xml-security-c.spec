Summary:        C++ XML Signature and Encryption library.
Name:           xml-security-c
Version:        2.0.4
Release:        4%{?dist}
URL:            https://santuario.apache.org/cindex.html
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

# You can download from other mirrors as well
# https://archive.apache.org/dist/santuario/c-library/%{name}-%{version}.tar.bz2
# For SRP compliance using git tag tarball here
Source0: https://github.com/apache/santuario-cpp/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:     Allow-use-of-md5-in-fips-mode.patch

Requires:       openssl
Requires:       xerces-c

BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  xerces-c-devel

%description
XML-Security-C is the C++ XML Signature and Encryption library from the Apache Software Foundation.
It is used for all XML Signature and Encryption processing in OpenSAML and Shibboleth.

%package    devel
Summary:    XML Security C library headers
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains development headers and static library for xml security.

%prep
%autosetup -p1 -n santuario-cpp-%{version}

%build
autoreconf -fiv
%configure \
    --disable-debug \
    --disable-static \
    --without-nss \
    --with-openssl

%make_build

%install
%make_install %{?_smp_mflags}

%check
./xsec/xsec-xtest

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%exclude %{_libdir}/libxml-security-c.la

%changelog
* Wed Feb 26 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.4-4
- Bump version as part of xerces-c upgrade
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.0.4-3
- Release bump for SRP compliance
* Tue Oct 25 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.0.4-2
- Bump version as part of xerces-c upgrade
* Wed Jan 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.4-1
- Upgrade to v2.0.4
- Abort when MD5 is used and fips enabled
* Mon Apr 12 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.2-3
- openssl 3.0.0 compatibility
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.2-2
- openssl 1.1.1
* Wed Jun 10 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.7.3-3
- Patch for gcc-6.3
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.3-2
- GA - Bump release of all rpms
* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 1.7.3-1
- Upgrade version.
* Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.5.1-1
- Initial version
