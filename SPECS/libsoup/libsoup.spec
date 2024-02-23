Summary:         libsoup HTTP client/server library
Name:            libsoup
Version:         3.2.1
Release:         12%{?dist}
License:         GPLv2
URL:             http://wiki.gnome.org/LibSoup
Group:           System Environment/Development
Vendor:          VMware, Inc.
Distribution:    Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/libsoup/3.2/%{name}-%{version}.tar.xz
%define sha512 %{name}=e5f60fd700f4cda041d869eec50e787b2fbe9323949b90710405cff296e108bab6d1323ab96e89855c5396ce73c7b7574b424dbe957ae10b48740b272889be51

BuildRequires: glib-devel
BuildRequires: libxml2-devel
BuildRequires: intltool
BuildRequires: python3-devel
BuildRequires: python3-tools
BuildRequires: glib-networking
BuildRequires: autogen
BuildRequires: sqlite-devel
BuildRequires: libpsl-devel
BuildRequires: krb5-devel
BuildRequires: httpd
BuildRequires: meson
BuildRequires: cmake
BuildRequires: nghttp2-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gnutls-devel

Requires: libxml2
Requires: glib-networking
Requires: sqlite-libs
Requires: libpsl
Requires: krb5
Requires: nghttp2

%description
libsoup is HTTP client/server library for GNOME

%package         devel
Summary:         Header files for libsoup
Group:           System Environment/Development
Requires:        %{name} = %{version}-%{release}
Requires:        glib-devel
Requires:        libxml2-devel
Requires:        sqlite-devel
Requires:        libpsl-devel
Requires:        nghttp2-devel

%description     devel
Header files for libsoup.

%package         lang
Summary:         Additional language files for libsoup
Group:           System Environment/Development
Requires:        %{name} = %{version}-%{release}

%description     lang
These are the additional language files of libsoup.

%prep
%autosetup -p1

%build
%meson \
    --auto-features=disabled \
    -D vapi=disabled

%meson_build

%install
%meson_install

%if 0%{?with_check}
%check
%meson_test
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files lang
%defattr(-,root,root)
%{_datadir}/locale/*

%changelog
* Fri Feb 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 3.2.1-12
- Bump version as a part of sqlite upgrade to v3.43.2
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.2.1-11
- Bump version as a part of gnutls upgrade
* Mon Oct 30 2023 Nitesh Kumar <kunitesh@vmware.com> 3.2.1-10
- Bump version as a part of httpd v2.4.58 upgrade
* Mon Oct 23 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.2.1-9
- Version bump as part of nghtttp2 upgrade
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 3.2.1-8
- Bump version as a part of krb5 upgrade
* Tue Jul 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.2.1-7
- Add nghttp2-devel to devel package requires
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.2.1-6
- Bump version as a part of libxml2 upgrade
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 3.2.1-5
- Bump version as a part of httpd v2.4.56 upgrade
* Tue Jan 31 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.2.1-4
- Bump version as a part of krb5 upgrade
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 3.2.1-3
- Bump version as a part of httpd v2.4.55 upgrade
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 3.2.1-2
- bump release as part of sqlite update
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.1-1
- Automatic Version Bump
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.0-1
- Upgrade to v3.2.0
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.72.0-5
- Bump version as a part of sqlite upgrade
* Mon Jun 20 2022 Nitesh Kumar <kunitesh@vmware.com> 2.72.0-4
- Bump version as a part of httpd v2.4.54 upgrade
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 2.72.0-3
- Improve Requires for main and -devel packages
- Remove icu dependencies as it will be brought by libpsl
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 2.72.0-2
- Release bump up to use libxml2 2.9.12-1.
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.72.0-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.71.1-1
- Automatic Version Bump
* Mon Aug 24 2020 Keerthana K <keerthanak@vmware.com> 2.71.0-1
- Update to version 2.71.0
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 2.64.0-3
- Build with python3
- Mass removal python2
* Fri Dec 07 2018 Keerthana <keerthanak@vmware.com> 2.64.0-2
- Fix Make check failures.
* Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 2.64.0-1
- Update to 2.64.0
* Mon Sep 03 2018 Ankit Jain <ankitja@vmware.com> 2.57.1-4
- Fix for CVE-2018-12910
* Mon Jun 18 2018 Tapas Kundu <tkundu@vmware.com> 2.57.1-3
- CVE-2017-2885
* Fri Aug 11 2017 Chang Lee <changlee@vmware.com> 2.57.1-2
- Added krb5-devel to BuildRequires for %check
* Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 2.57.1-1
- Upgrading to version 2.57.1
* Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> 2.53.90-3
- Add sqlite-devel build deps
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.53.90-2
- GA - Bump release of all rpms
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 2.53.90-1
- Updated version.
* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.50.0-5
- Moving static lib files to devel package.
* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 2.50.0-4
- Removing la files from packages.
* Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 2.50.0-3
- Addinf libxml2 to Requires
* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 2.50.0-2
- Exclude /usr/lib/debug
* Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 2.50.0-1
- Initial build.  First version
