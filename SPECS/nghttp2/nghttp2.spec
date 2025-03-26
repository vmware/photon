Summary:        nghttp2 is an implementation of HTTP/2 and its header compression algorithm, HPACK.
Name:           nghttp2
Version:        1.57.0
Release:        3%{?dist}
URL:            https://nghttp2.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Patch0:  CVE-2024-28182.patch

BuildRequires:  c-ares-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  libevent-devel
BuildRequires:  jansson-devel

Provides: pkgconfig(libnghttp2)

%description
Implementation of the Hypertext Transfer Protocol version 2 in C.

%package        devel
Summary:        Header files for nghttp2
Requires:       %{name} = %{version}-%{release}

%description    devel
These are the header files of nghttp2.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --enable-lib-only \
    --disable-python-bindings

%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datadir}/nghttp2
%{_docdir}/%{name}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.57.0-3
- Release bump for SRP compliance
* Fri Apr 05 2024 Harinadh D <hdommaraju@vmware.com> 1.57.0-2
- Fix for CVE-2024-28182
* Mon Oct 23 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.57.0-1
- Upgrade to version 1.57.0
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.48.0-4
- Bump version as a part of libxml2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.48.0-3
- Bump version as a part of zlib upgrade
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.48.0-2
- Fix provides
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.48.0-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.47.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.43.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.41.0-2
- openssl 1.1.1
* Tue Jul 07 2020 Gerrit Photon <photon-checkins@vmware.com> 1.41.0-1
- Automatic Version Bump
* Wed Jun 24 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.33.0-2
- Used configure macro
* Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.33.0-1
- Upgrade to version 1.33.0
* Tue Jun 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.23.1-1
- First version.
