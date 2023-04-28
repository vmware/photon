Summary:        Libxslt
Name:           libxslt
Version:        1.1.37
Release:        3%{?dist}
License:        MIT
URL:            http://http://xmlsoft.org/libxslt
Group:          System Environment/General Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://download.gnome.org/sources/%{name}/1.1/%{name}-%{version}.tar.gz
%define sha512 %{name}=4e7a57cbe02ceea34404213a88bdbb63a756edfab63063ce3979b670816ae3f6fb3637a49508204e6e46b936628e0a3b8b77e9201530a1184225bd68da403b25

Requires:       libxml2
Requires:       libgcrypt
Requires:       libgpg-error

BuildRequires:  automake >= 1.16.5
BuildRequires:  libxml2-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error-devel

%description
The libxslt package contains XSLT libraries used for extending libxml2 libraries to support XSLT files.

%package devel
Summary:        Development Libraries for libxslt
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libxml2-devel

%description devel
Header files for doing development with libxslt.

%prep
%autosetup -p1
sed -i 's/int xsltMaxDepth = 3000/int xsltMaxDepth = 5000/g' libxslt/transform.c

%build
autoreconf -vfi
%configure \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    --disable-static \
    --without-python

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.sh
%{_libdir}/libxslt-plugins
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_libdir}/cmake/libxslt/*
%{_includedir}/*
%{_docdir}/*
%{_datadir}/aclocal/*
%{_mandir}/man3/*
%{_datadir}/gtk-doc/*

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.37-3
- Bump version as a part of libxml2 upgrade
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1.37-2
- Bump release as a part of libgpg-error upgrade to 1.46
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.37-1
- Upgrade to v1.1.37
* Thu Oct 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.35-3
- Fix requires
* Sun Jul 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.35-2
- Add libgpg-error-devel to BuildRequires
* Mon Jun 20 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.35-1
- Update to version 1.1.35
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 1.1.34-4
- Release bump up to use libxml2 2.9.12-1.
* Fri Feb 19 2021 Shreyas B. <shreyasb@vmware.com> 1.1.34-3
- Increase the maximum number of nested template calls for xml.
* Fri Dec 18 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.34-2
- Fix build with new rpm
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.34-1
- Automatic Version Bump
* Tue Dec 17 2019 Shreyas B. <shreyasb@vmware.com> 1.1.32-3
- Apply patch for CVE-2019-5815: READ heap-buffer-overflow in libxslt.
- Apply patch for CVE-2019-18197
- Apply patch for CVE-2019-13118
- Apply patch for CVE-2019-13117
- Apply patch for CVE-2019-11068
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.32-2
- Cross compilation support
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.1.32-1
- Update to version 1.1.32.
* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 1.1.29-4
- Applied patches for CVE-2015-9019 and CVE-2017-5029.
* Tue May 23 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1.29-3
- Build does not requires python.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.29-2
- Moved man3 to devel subpackage.
* Fri Oct 21 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.29-1
- Fix CVEs 2016-1683, 2016-1684, 2015-7995 with version 1.1.29
* Mon Oct 03 2016 Chang Lee <changlee@vmware.com> 1.1.28-4
- Modified check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.28-3
- GA - Bump release of all rpms
* Tue Jan 19 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.28-2
- Add a dev subpackage.
* Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.28-1
- Initial build.  First version
