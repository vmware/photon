Summary:        Basic and advanced IPV4-based networking
Name:           iproute2
Version:        4.18.0
Release:        1%{?dist}
License:        GPLv2+
URL:            http://www.kernel.org/pub/linux/utils/net/iproute2
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.kernel.org/pub/linux/utils/net/iproute2/%{name}-%{version}.tar.xz
%define sha1    iproute2=ff02c7352bae407a76d71b36558700bb489026fc
Patch0:         replace_killall_by_pkill.patch

%description
The IPRoute2 package contains programs for basic and advanced
IPV4-based networking.

%package devel
Summary: Header files for building application using iproute2.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q
sed -i /ARPD/d Makefile
sed -i 's/arpd.8//' man/man8/Makefile
sed -i 's/m_ipt.o//' tc/Makefile
%patch0 -p1

%build
make VERBOSE=1 %{?_smp_mflags} DESTDIR= LIBDIR=%{_libdir}
%install
make    DESTDIR=%{buildroot} \
    MANDIR=%{_mandir} \
    LIBDIR=%{_libdir} \
    DOCDIR=%{_defaultdocdir}/%{name}-%{version} install

%check
cd testsuite
# Fix linking issue in testsuite
sed -i 's/<libnetlink.h>/\"..\/..\/include\/libnetlink.h\"/g' tools/generate_nlmsg.c
sed -i 's/\"libnetlink.h\"/"..\/include\/libnetlink.h\"/g' ../lib/libnetlink.c
cd tools
make
cd ..
make
make alltests
cd ..

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_sysconfdir}/%{name}/*
/sbin/*
%{_libdir}/tc/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/tc

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/bpf_elf.h
%{_mandir}/man3/*

%changelog
*   Wed Sep 05 2018 Ankit Jain <ankitja@vmware.com> 4.18.0-1
-   Updated to version 4.18.0
*   Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> 4.10.0-3
-   Fix compilation issue for glibc-2.26
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 4.10.0-2
-   Move man3 to devel package.
*   Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.10.0-1
-   Updated to version 4.10.0
*   Thu Jun 16 2016 Nick Shi <nshi@vmware.com> 4.2.0-3
-   Replace killall by pkill in ifcfg
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.0-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 4.2.0-1
-   Updated to version 4.2.0
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.12.0-1
-   Initial build. First version
