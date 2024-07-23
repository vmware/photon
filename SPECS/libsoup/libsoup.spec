%define maj_ver 2.72

Summary:         libsoup HTTP client/server library
Name:            libsoup
Version:         2.72.0
Release:         13%{?dist}
License:         GPLv2
URL:             http://wiki.gnome.org/LibSoup
Group:           System Environment/Development
Vendor:          VMware, Inc.
Distribution:    Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/libsoup/%{maj_ver}/%{name}-%{version}.tar.xz
%define sha512 %{name}=ca16772d0d318c4be0c4859db1e32baffa2231b4732f3bf9814aa405febde86395a0fb8bfa1635d70a7b5853d2567403920b9b0d0f5c3c179294352af27e91de

%if 0%{?with_check}
Patch0: libsoup-fix-make-check.patch
Patch1: libsoup-issue-120.patch
%endif

BuildRequires: glib-devel >= 2.68.4
BuildRequires: gobject-introspection
BuildRequires: libxml2-devel
BuildRequires: intltool
BuildRequires: python3
BuildRequires: python3-libs
BuildRequires: python3-devel
BuildRequires: python3-tools
BuildRequires: glib-networking
BuildRequires: autogen
BuildRequires: sqlite-devel
BuildRequires: libpsl-devel
BuildRequires: krb5-devel
BuildRequires: httpd
BuildRequires: meson >= 0.50
BuildRequires: ninja-build
BuildRequires: gtk-doc
BuildRequires: cmake

Requires: libxml2
Requires: glib-networking
Requires: sqlite-libs
Requires: libpsl
Requires: krb5

%description
libsoup is HTTP client/server library for GNOME

%package         devel
Summary:         Header files for libsoup
Group:           System Environment/Development
Requires:        %{name} = %{version}-%{release}
Requires:        glib-devel >= 2.68.4
Requires:        libxml2-devel
Requires:        sqlite-devel
Requires:        libpsl-devel

%description     devel
Header files for libsoup.

%package         doc
Summary:         gtk-doc files for libsoup
Group:           System Environment/Development
Requires:        %{name} = %{version}-%{release}

%description     doc
gtk-doc files for libsoup.

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
    --auto-features=auto

%meson_build

%install
%meson_install

%find_lang %{name}

%if 0%{?with_check}
%check
%meson_test
%endif

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files doc
%defattr(-,root,root)

%changelog
* Tue Jul 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.72.0-13
- Version Bump up to consume httpd v2.4.62
* Tue Jul 09 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.72.0-12
- Version Bump up to consume httpd v2.4.61
* Fri Apr 05 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.72.0-11
- Version Bump up to consume httpd v2.4.59
* Mon Oct 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.72.0-10
- Bump version as a part of httpd v2.4.58 upgrade
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.72.0-9
- Bump version as part of glib upgrade
* Thu May 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.72.0-8
- Use meson macros for building
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 2.72.0-7
- Bump version as a part of httpd v2.4.56 upgrade
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.72.0-6
- Bump version as a part of httpd v2.4.55 upgrade
* Tue Jun 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.72.0-5
- Bump version as a part of sqlite upgrade
* Mon Jun 20 2022 Nitesh Kumar <kunitesh@vmware.com> 2.72.0-4
- Bump version as a part of httpd v2.4.54 upgrade
* Tue Dec 07 2021 Alexey Makhalov <amakhalov@vmware.com> 2.72.0-3
- Improve Requires for main and -devel packages
- Remove icu dependencies as it will be brought by libpsl
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 2.72.0-2
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
