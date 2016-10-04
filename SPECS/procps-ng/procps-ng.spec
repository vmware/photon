Summary:	Programs for monitoring processes
Name:		procps-ng
Version:	3.3.11
Release:	4%{?dist}
License:	GPLv2
URL:		http://procps.sourceforge.net/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://sourceforge.net/projects/procps-ng/files/Production/%{name}-%{version}.tar.xz
%define sha1 procps-ng=1bdca65547df9ed019bd83649b0f8b8eaa017e25
Patch0:		Fixto-interpret-ascii-sequence.patch
BuildRequires:	ncurses-devel
Requires:	ncurses
%description
The Procps package contains programs for monitoring processes.
%package	devel
Summary:	Header and development files for procps-ng
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q
%patch0 -p1
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

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
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
%{_docdir}/procps-ng-3.3.11/FAQ
%{_docdir}/procps-ng-3.3.11/bugs.md
%{_mandir}/man8/vmstat.8.gz
%{_mandir}/man8/sysctl.8.gz
%{_mandir}/man1/slabtop.1.gz
%{_mandir}/man1/free.1.gz
%{_mandir}/man1/pmap.1.gz
%{_mandir}/man1/pwdx.1.gz
%{_mandir}/man1/tload.1.gz
%{_mandir}/man1/top.1.gz
%{_mandir}/man1/pgrep.1.gz
%{_mandir}/man1/uptime.1.gz
%{_mandir}/man1/pkill.1.gz
%{_mandir}/man1/pidof.1.gz
%{_mandir}/man1/w.1.gz
%{_mandir}/man1/watch.1.gz
%{_mandir}/man1/ps.1.gz
%{_mandir}/man3/*
%{_mandir}/man5/sysctl.conf.5.gz
%{_libdir}/libprocps.so.5
%{_libdir}/libprocps.so.5.0.0
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
%{_libdir}/pkgconfig/libprocps.pc
%{_libdir}/libprocps.so
%changelog
*       Mon Oct 03 2016 ChangLee <changLee@vmware.com> 3.3.11-4
-       Modified %check
*	Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.11-3
-	Added patch to interpret ASCII sequence correctly
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.11-2
-	GA - Bump release of all rpms
*	Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 3.3.11-1
-	Upgrade version
*   	Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.3.9-2
-   	Update according to UsrMove.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3.9-1
-	Initial build. First version
