Summary:        Grep for perl compatible regular expressions
Name:           pcre
Version:        8.42
Release:        1%{?dist}
License:        BSD
URL:            ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{version}.tar.bz2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.bz2
%define sha1    pcre=df0d1c2ff04c359220cb902539a6e134af4497f4
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
Requires:       libgcc
Requires:       readline
Requires:       libstdc++
Requires:       pcre-libs = %{version}-%{release}
%description
The PCRE package contains Perl Compatible Regular Expression libraries. These are useful for implementing regular expression pattern matching using the same syntax and semantics as Perl 5.

%package        devel
Group:          Development/Libraries
Summary:        Headers and static lib for pcre development
Requires:       %{name} = %{version}-%{release}
Provides:       pkgconfig(libpcre)
%description    devel
Install this package if you want do compile applications using the pcre
library.

%package libs
Summary: Libraries for pcre
Group:      System Environment/Libraries
%description libs
This package contains minimal set of shared pcre libraries.

%prep
%setup -q
%build
./configure --prefix=/usr                     \
            --docdir=/usr/share/doc/pcre-%{version} \
            --enable-unicode-properties       \
            --enable-pcre16                   \
            --enable-pcre32                   \
            --enable-pcregrep-libz            \
            --enable-pcregrep-libbz2          \
            --enable-pcretest-libreadline     \
            --with-match-limit-recursion=16000 \
            --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mv -v %{buildroot}/usr/lib/libpcre.so.* %{buildroot}/lib &&
ln -sfv ../../lib/$(readlink %{buildroot}/usr/lib/libpcre.so) %{buildroot}/usr/lib/libpcre.so
ln -sfv $(readlink %{buildroot}/usr/lib/libpcre.so) %{buildroot}/usr/lib/libpcre.so.0

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_bindir}/pcregrep
%{_bindir}/pcretest
%{_mandir}/man1/pcregrep.1*
%{_mandir}/man1/pcretest.1*
%{_libdir}/*.so.*
%exclude %{_libdir}/libpcre.so.*

%files devel
%defattr(-, root, root)
%{_bindir}/*
%exclude %{_bindir}/pcregrep
%exclude %{_bindir}/pcretest
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%files libs
%defattr(-, root, root)
%{_libdir}/libpcre.so.*

%changelog
*   Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 8.42-1
-   Update to version 8.42
*   Wed Dec 20 2017 Xiaolin Li <xiaolinl@vmware.com> 8.41-1
-   Update to version 8.41
*   Wed Jul 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 8.40-4
-   Added fix for CVE-2017-11164 by adding stack recursion limit
*   Wed May 24 2017 Divya Thaluru <dthaluru@vmware.com> 8.40-3
-   Added fixes for CVE-2017-7244, CVE-2017-7245, CVE-2017-7246, CVE-2017-7186
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 8.40-2
-   Added -libs subpackage
*   Mon Apr 03 2017 Robert Qi <qij@vmware.com> 8.40-1
-   Update to 8.40
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 8.39-2
-   Modified %check
*   Fri Sep 9 2016 Xiaolin Li <xiaolinl@vmware.com> 8.39-1
-   Update to version 8.39
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.38-3
-   GA - Bump release of all rpms
*   Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com>  8.38-2
-   Add upstream fixes patch
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 8.38-1
-   Updated to version 8.38
*   Mon Nov 30 2015 Sharath George <sharathg@vmware.com> 8.36-2
    Add symlink for libpcre.so.1
*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 8.36-1
    Initial version
