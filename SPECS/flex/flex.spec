Summary:    A utility for generating programs that recognize patterns in text
Name:       flex
Version:    2.6.4
Release:    4%{?dist}
URL:        https://github.com/westes/flex/releases
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/westes/flex/releases/%{name}-%{version}.tar.gz
%define sha512 %{name}=e9785f3d620a204b7d20222888917dc065c2036cae28667065bf7862dfa1b25235095a12fd04efdbd09bfd17d3452e6b9ef953a8c1137862ff671c97132a082e

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  m4

Requires:   m4

%description
The Flex package contains a utility for generating programs
that recognize patterns in text.

%package devel
Summary: Development libraries and header files for the flex library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The flex-devel package contains the development libraries and header files for
flex.

%prep
%autosetup -p1
sed -i -e '/test-bison/d' tests/Makefile.in
sed -i "/math.h/a #include <malloc.h>" src/flexdef.h

%build
autoreconf -fiv
%configure \
    --docdir=%{_docdir}/%{name}-%{version} \
    --disable-silent-rules

make VERBOSE=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete
cat > %{buildroot}/usr/bin/lex <<- "EOF"
#!/bin/sh
# Begin /usr/bin/lex

exec /usr/bin/flex -l "$@"

# End /usr/bin/lex
EOF
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/flex
%{_bindir}/flex++
%attr(755,root,root) %{_bindir}/lex
%{_libdir}/*.so.*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*

%changelog
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.6.4-4
-   Release bump for SRP compliance
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 2.6.4-3
-   Cross compilation support
*   Fri Aug 4 2017 Alexey Makhalov <amakhalov@vmware.com> 2.6.4-2
-   Use _GNU_SOURCE
*   Thu May 11 2017 Chang Lee <changlee@vmware.com> 2.6.4-1
-   Updated to version 2.6.4
*   Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 2.6.0-1
-   Updated to version 2.6.0
*   Thu Oct 13 2016 Kumar Kaushik <kaushikk@vmware.com> 2.5.39-3
-   Fixing Security bug CVE-2016-6354.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.39-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5.39-1
-   Updated to version 2.5.39
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.5.38-3
-   Moving static lib files to devel package.
*   Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 2.5.38-2
-   Adding m4 package to build and run time required package
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.5.38-1
-   Initial build. First version
