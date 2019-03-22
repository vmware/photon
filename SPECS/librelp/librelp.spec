Summary:        RELP Library
Name:           librelp
Version:        1.2.17
Release:        3%{?dist}
License:        GPLv3+
URL:            http://www.librelp.com
Source0:        http://download.rsyslog.com/librelp/%{name}-%{version}.tar.gz
%define sha1 librelp=701d69e7723fe614b96750af8cba5ee9a54085fe
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  gnutls-devel
BuildRequires:  autogen
Requires:       gnutls
Requires:       gmp
%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%package devel
Summary:        Development libraries and header files for librelp
Requires:       librelp

%description devel
The package contains libraries and header files for
developing applications that use librelp.

%prep
%setup -q
autoreconf -fiv
%build
./configure \
        --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libdir}/*.a
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*   Fri Mar 22 2019 Keerthana K <keerthanak@vmware.com> 1.2.17-1
-   Updated to version 1.2.17
*   Fri Apr 20 2018 Xiaolin Li <xiaolinl@vmware.com> 1.2.9-3
-   Fix CVE-2018-1000140
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.9-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.2.9-1
-   Upgrade to 1.2.9
*   Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.2.7-1
-   Initial build. First version

