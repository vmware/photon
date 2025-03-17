Summary:    Programs to parse command-line options
Name:       popt
Version:    1.16
Release:    7%{?dist}
URL:        http://rpm5.org/files/popt
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.rpm.org/mirror/popt/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
The popt package contains the popt libraries which are used by
some programs to parse command-line options.

%package devel
Summary:    Libraries and header files for popt
Requires:   %{name} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for popt

%package lang
Summary: Additional language files for popt
Group:      Applications/System
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of popt.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libpopt.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/popt.pc
%{_libdir}/libpopt.a
%{_libdir}/libpopt.so
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.16-7
-   Release bump for SRP compliance
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.16-6
-   Release bump for SRP compliance
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.16-5
-   Use standard configure macros
*   Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 1.16-4
-   Added -lang subpackage
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.16-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16-2
-   GA - Bump release of all rpms
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.16-1
-   Initial build. First version
