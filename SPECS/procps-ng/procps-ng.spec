Summary:	Programs for monitoring processes
Name:		procps-ng
Version:	3.3.9
Release:	2%{?dist}
License:	GPLv2
URL:		http://procps.sourceforge.net/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://sourceforge.net/projects/procps-ng/files/Production/%{name}-%{version}.tar.xz
%define sha1 procps-ng=088c77631745fc75ee41fc29c254a4069be4869a
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
mv -v %{buildroot}/usr/bin/pidof %{buildroot}/bin
ln -sfv ../..%{_lib}/$(readlink %{buildroot}/%{_libdir}/libprocps.so) %{buildroot}/%{_libdir}/libprocps.so
find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
/bin/ps
/bin/pidof
%{_bindir}/free
%{_bindir}/w
%{_bindir}/pgrep
%{_bindir}/uptime
%{_bindir}/vmstat
%{_bindir}/pmap
%{_bindir}/tload
%{_bindir}/pwdx
%{_bindir}/top
%{_bindir}/slabtop
%{_bindir}/watch
%{_bindir}/pkill
%{_docdir}/procps-ng-3.3.9/FAQ
%{_docdir}/procps-ng-3.3.9/README.top
%{_docdir}/procps-ng-3.3.9/BUGS
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
%{_mandir}/man5/sysctl.conf.5.gz
%{_libdir}/libprocps.so.3
%{_libdir}/libprocps.so.3.0.0
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
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.3.9-2
-   Update according to UsrMove.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3.9-1
-	Initial build. First version
