%define sourcever 3380500

Summary:        A portable, high level programming interface to various calling conventions
Name:           sqlite
Version:        3.38.5
Release:        5%{?dist}
License:        Public Domain
URL:            http://www.sqlite.org
Group:          System Environment/GeneralLibraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://sqlite.org/2020/%{name}-autoconf-%{sourcever}.tar.gz
%define sha512 %{name}=6f515a7782bfb5414702721fc78ada5bf388f4bf8b3e3c2ec269df33a2e372859f682d028c30084e89847705c7050ea80790d51fbcc4decea8fbb0a35b89c0b3

Patch0:         0001-Fix-for-CVE-2022-46908.patch
Patch1:         Fix-CLI-seg-fault-on-missing-nonce.patch
Patch2:         CVE-2023-7104.patch
Patch3:         CVE-2025-29088.patch

Obsoletes:      sqlite-autoconf
Obsoletes:      sqlite-devel <= 3.27.2-5
Requires:       sqlite-libs = %{version}-%{release}
Provides:       sqlite3

%description
This package contains most of the static files that comprise the
www.sqlite.org website including all of the SQL Syntax and the
C/C++ interface specs and other miscellaneous documentation.

%package        devel
Summary:        sqlite3 link library & header files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The sqlite devel package include the needed library link and
header files for development.

%package        libs
Summary:        sqlite3 library
Group:          Libraries
Provides:       pkgconfig(sqlite3)
Obsoletes:      libsqlite
Obsoletes:      sqlite-autoconf

%description    libs
The sqlite3 library.

%prep
%autosetup -p1 -n %{name}-autoconf-%{sourcever}

%build
export CFLAGS="%{optflags} \
           -DSQLITE_ENABLE_FTS3=1 \
           -DSQLITE_ENABLE_COLUMN_METADATA=1 \
           -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 \
           -DSQLITE_SECURE_DELETE=1"

%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}
install -D -m644 sqlite3.1 %{buildroot}%{_mandir}/man1/sqlite3.1
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}
%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/libsqlite3.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/libsqlite3.so.0.8.6
%{_libdir}/libsqlite3.so.0

%changelog
* Mon Apr 28 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.38.5-5
- Fix CVE-2025-29088
* Tue Jan 09 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 3.38.5-4
- Patched CVE-2023-7104
* Fri Aug 25 2023 Kuntal Nayak <nkuntal@vmware.com> 3.38.5-3
- Fix for CVE-2023-36191
* Wed Dec 14 2022 Srish Srinivasan <ssrish@vmware.com> 3.38.5-2
- Fix for CVE-2022-46908
* Tue Jun 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.38.5-1
- Upgrade to v3.38.5 to fix CVE-2021-20227
* Fri Aug 28 2020 Gerrit Photon <photon-checkins@vmware.com> 3.33.0-1
- Automatic Version Bump
* Fri Jul 03 2020 Shreyas B <shreyasb@vmware.com> 3.32.1-1
- Upgrade to 3.32.1 & fix CVE-2020-15358
- CVE-2020-13630 CVE-2020-13434 CVE-2020-13435 CVE-2020-13631 CVE-2020-13632
* Thu May 14 2020 Ankit Jain <ankitja@vmware.com> 3.31.1-1
- Updated to 3.31.1
* Sun Feb 3 2019 Michelle Wang <michellew@vmware.com> 3.26.0-1
- Upgrade to 3.26.0 for a critical Vulnerability named 'Magallan'.
* Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 3.25.1-1
- Upgrade to version 3.25.1
* Tue Feb 20 2018 Xiaolin Li <xiaolinl@vmware.com> 3.22.0-1
- Upgrade to version 3.22.0
* Fri Nov 10 2017 Xiaolin Li <xiaolinl@vmware.com> 3.21.0-1
- Upgrade to version 3.21.0
* Fri Jul 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.19.3-1
- Upgrading to version 3.19.0 and adding patch for CVE-2017-10989
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 3.18.0-2
- Added obseletes for deprecated sqlite-autoconf package
* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 3.18.0-1
- Version update
- Package rename: sqlite-autoconf -> sqlite
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.11.0-4
- Added -devel and -libs subpackages
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.11.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11.0-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.11.0-1
- Updated to version 3.11.0
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 3.8.3.1-2
- Fix versioning
* Tue Oct 7 2014 Divya Thaluru <dthaluru@vmware.com> 3080301-1
- Initial build. First version
