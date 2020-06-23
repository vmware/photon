Summary:        Grep for perl compatible regular expressions
Name:           pcre
Version:        8.44
Release:        1%{?dist}
License:        BSD
URL:            ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.41.tar.bz2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://ftp.pcre.org/pub/pcre/%{name}-%{version}.tar.bz2
%define sha1    pcre=8179b083053fce9b4a766513fa1f14807aabee42
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
Requires:       libgcc
Requires:       libstdc++
%description
The PCRE package contains Perl Compatible Regular Expression libraries. These are useful for implementing regular expression pattern matching using the same syntax and semantics as Perl 5.

%package        devel
Group:          Development/Libraries
Summary:        Headers and static lib for pcre development
Requires:       %{name} = %{version}
Provides:       pkgconfig(libpcre)
%description    devel
Install this package if you want do compile applications using the pcre
library.

%prep
%setup -q
%build
%configure --docdir=/usr/share/doc/pcre-%{version} \
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
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/pcregrep  
%{_bindir}/pcretest
%{_mandir}/man1/pcregrep.1*
%{_mandir}/man1/pcretest.1*
%{_libdir}/*.so.*

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
%changelog
*   Mon Jun 22 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 8.44-1
-   Update to 8.44
*   Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 8.41-2
-   Fix for CVE-2017-11164 by adding stack recursion limit.
*   Wed Dec 20 2017 Xiaolin Li <xiaolinl@vmware.com> 8.41-1
-   Update to version 8.41
*   Fri Sep 09 2016 Xiaolin Li <xiaolinl@vmware.com> 8.39-1
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
