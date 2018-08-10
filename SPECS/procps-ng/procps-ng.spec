Summary:        Programs for monitoring processes
Name:           procps-ng
Version:        3.3.15
Release:        1%{?dist}
License:        GPLv2
URL:            http://procps.sourceforge.net/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sourceforge.net/projects/procps-ng/files/Production/%{name}-%{version}.tar.xz
%define sha1    procps-ng=2929bc64f0cf7b2db997eef79b7187658e47230d
BuildRequires:  ncurses-devel
Requires:       ncurses
Conflicts:      toybox
%description
The Procps package contains programs for monitoring processes.
%package    devel
Summary:    Header and development files for procps-ng
Requires:   %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications 

%package lang
Summary: Additional language files for procps-ng
Group:   Applications/Databases
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of procps-ng

%prep
%setup -q
%build
./configure \
    --prefix=%{_prefix} \
    --exec-prefix= \
    --libdir=%{_libdir} \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-static \
    --disable-kill \
    --disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
install -vdm 755 %{buildroot}/%{_lib}
ln -sfv ../..%{_lib}/$(readlink %{buildroot}/%{_libdir}/libprocps.so) %{buildroot}/%{_libdir}/libprocps.so
install -vdm 755 %{buildroot}/%{_sbindir}
ln -s %{_bindir}/pidof %{buildroot}%{_sbindir}/pidof
find %{buildroot} -name '*.la' -delete
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
/bin/ps
/bin/pidof
/bin/free
/bin/w
/bin/pgrep
/bin/uptime
/bin/vmstat
/bin/pmap
/bin/tload
/bin/pwdx
/bin/top
/bin/slabtop
/bin/watch
/bin/pkill
%{_sbindir}/pidof
%_datadir/locale/*
%{_docdir}/procps-ng-*/*
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/libprocps.so.*
/sbin/sysctl
%files devel
%{_includedir}/proc/sig.h
%{_includedir}/proc/wchan.h
%{_includedir}/proc/version.h
%{_includedir}/proc/pwcache.h
%{_includedir}/proc/procps.h
%{_includedir}/proc/devname.h
%{_includedir}/proc/sysinfo.h
%{_includedir}/proc/readproc.h
%{_includedir}/proc/escape.h
%{_includedir}/proc/slab.h
%{_includedir}/proc/alloc.h
%{_includedir}/proc/whattime.h
%{_includedir}/proc/numa.h
%{_libdir}/pkgconfig/libprocps.pc
%{_libdir}/libprocps.so
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Fri Aug 10 2018 Tapas Kundu <tkundu@vmware.com> 3.3.15-1
-   Upgrade version to 3.3.15.
-   Fix for CVE-2018-1122 CVE-2018-1123 CVE-2018-1124 CVE-2018-1125
-   Fix for CVE-2018-1126
*   Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 3.3.12-3
-   Added conflicts toybox
*   Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 3.3.12-2
-   Add lang package.
*   Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 3.3.12-1
-   Upgrade to 3.3.12
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 3.3.11-5
-   Moved man3 to devel subpackage.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 3.3.11-4
-   Modified %check
*   Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.11-3
-   Added patch to interpret ASCII sequence correctly
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.11-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 3.3.11-1
-   Upgrade version
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.3.9-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3.9-1
-   Initial build. First version
