%define        with_boost     1
%define        with_crash     1
%define        with_docs      0
%define        with_grapher   0
%define        with_pie       1
%define        with_rpm       0
%define        with_sqlite    1

Name:          systemtap
Version:       3.0
Release:       4%{?dist}
Summary:       Programmable system-wide instrumentation system
Group:         Development/System
Vendor:	       VMware, Inc.
Distribution:  Photon
URL:           http://sourceware.org/systemtap/
Source0:       http://sourceware.org/systemtap/ftp/releases/systemtap-%{version}.tar.gz
%define sha1 systemtap=5ef3a2d9945b0f6bae0061e33811e25e5138f5b7
License:       GPLv2+

BuildRequires: elfutils-devel
BuildRequires: glibc-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: libgcc
BuildRequires: nspr
BuildRequires: nss-devel
BuildRequires: sqlite-devel
BuildRequires: libstdc++-devel
BuildRequires: libtirpc-devel
BuildRequires: libxml2-devel
BuildRequires: perl
BuildRequires: nss
%if %with_boost 
BuildRequires: boost-devel
%endif
%if %with_crash
BuildRequires: crash-devel
BuildRequires: zlib-devel
Requires:      crash
%endif
BuildRequires: pkg-config
%if %with_rpm
BuildRequires: rpm-devel
%endif
Requires:      gcc
Requires:      linux-devel
Requires:      make
Requires:      elfutils
Requires:      %{name}-runtime = %{?epoch:%epoch:}%{version}-%{release}
Requires:      shadow

BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system.  The base systemtap package contains/requires
the components needed to locally develop and execute systemtap scripts.


%package initscript
Group:         System/Tools
Summary:       Systemtap Initscript
Requires:      %{name}-runtime = %{?epoch:%epoch:}%{version}-%{release}
Requires:      initscripts

%description initscript
Initscript for Systemtap scripts.

%package runtime
Group:         System/Tools
Summary:       Instrumentation System Runtime
Requires:      linux-devel

%description runtime
SystemTap runtime is the runtime component of an instrumentation system for systems running Linux.

%package sdt-devel
Group:         System/Tools
Summary:       Static probe support tools

%description sdt-devel
Support tools to allow applications to use static probes.

%package server
Group:         System/Tools
Summary:       Instrumentation System Server
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
Requires:      %{name}-runtime = %{?epoch:%epoch:}%{version}-%{release}
Requires:      coreutils
Requires:      nss
Requires:      unzip
Requires:      gzip

%description server
SystemTap server is the server component of an instrumentation system for systems running Linux.


%prep
%setup -q
sed -i "s#"kernel"#"linux"#g" stap-prep
sed -i "s#"devel"#"dev"#g" stap-prep

%build
%configure \
%if %with_crash
	--enable-crash \
%else
	--disable-crash \
%endif
	--disable-docs \
%if %with_sqlite
	--enable-sqlite \
%else
	--disable-sqlite \
%endif
%if %with_rpm
	--with-rpm \
%else
	--without-rpm \
%endif
%if %with_pie
	--enable-pie \
%else
	--disable-pie \
%endif
	--disable-grapher \
        --disable-virt \
	--disable-silent-rules

make

%install
[ "%{buildroot}" != / ] && rm -rf ""
%makeinstall

mv %{buildroot}%{_datadir}/doc/systemtap/examples examples

find examples -type f -name '*.stp' -print0 | xargs -0 sed -i -r -e '1s@^#!.+stap@#!%{_bindir}/stap@'

chmod 755 %{buildroot}%{_bindir}/staprun

install -c -m 755 stap-prep %{buildroot}%{_bindir}/stap-prep


mkdir -p %{buildroot}%{_sysconfdir}//rc.d/init.d/
install -m 755 initscript/systemtap %{buildroot}%{_sysconfdir}/rc.d/init.d/
mkdir -p %{buildroot}%{_sysconfdir}/systemtap
mkdir -p %{buildroot}%{_sysconfdir}/systemtap/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/systemtap/script.d
install -m 644 initscript/config.systemtap %{buildroot}%{_sysconfdir}/systemtap/config
mkdir -p %{buildroot}%{_localstatedir}/cache/systemtap
mkdir -p %{buildroot}%{_localstatedir}/run/systemtap

%if %with_docs
mkdir docs.installed
mv %{buildroot}%{_datadir}/doc/systemtap/*.pdf docs.installed/
mv %{buildroot}%{_datadir}/doc/systemtap/tapsets docs.installed/
%if %with_publican
mv %{buildroot}%{_datadir}/doc/systemtap/SystemTap_Beginners_Guide docs.installed/
%endif
%endif

install -m 755 initscript/stap-server %{buildroot}%{_sysconfdir}/rc.d/init.d/
mkdir -p %{buildroot}%{_sysconfdir}/stap-server
mkdir -p %{buildroot}%{_sysconfdir}/stap-server/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 initscript/config.stap-server %{buildroot}%{_sysconfdir}/sysconfig/stap-server
mkdir -p %{buildroot}%{_localstatedir}/log/stap-server
touch %{buildroot}%{_localstatedir}/log/stap-server/log
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 initscript/logrotate.stap-server %{buildroot}%{_sysconfdir}/logrotate.d/stap-server

%find_lang %{name}

%check
make %{?_smp_mflags} check

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%pre
getent group stap-server >/dev/null || groupadd -g 155 -r stap-server || groupadd -r stap-server

%pre runtime
getent group stapdev >/dev/null || groupadd -r stapdev
getent group stapusr >/dev/null || groupadd -r stapusr
exit 0

%pre server
getent passwd stap-server >/dev/null || \
/usr/sbin/useradd -c "Systemtap Compile Server" -u 155 -g stap-server -d %{_localstatedir}/lib/stap-server -m -r -s /sbin/nologin stap-server || \
/usr/sbin/useradd -c "Systemtap Compile Server" -g stap-server -d %{_localstatedir}/lib/stap-server -m -r -s /sbin/nologin stap-server
test -e ~stap-server && chmod 755 ~stap-server
exit 0

%post server
if [ $1 -eq 1 ] ; then
  test -e %{_localstatedir}/log/stap-server/log || {
  touch %{_localstatedir}/log/stap-server/log
  chmod 664 %{_localstatedir}/log/stap-server/log
  chown stap-server:stap-server %{_localstatedir}/log/stap-server/log
  }

  if test ! -e ~stap-server/.systemtap/ssl/server/stap.cert; then
	runuser -s /bin/sh - stap-server -c %{_libexecdir}/%{name}/stap-gen-cert >/dev/null

	%{_bindir}/stap-authorize-server-cert ~stap-server/.systemtap/ssl/server/stap.cert
	%{_bindir}/stap-authorize-signing-cert ~stap-server/.systemtap/ssl/server/stap.cert
  fi
  /sbin/chkconfig --add stap-server
  exit 0
fi

%preun server
if [ $1 = 0 ] ; then
	/sbin/service stap-server stop >/dev/null 2>&1
	/sbin/chkconfig --del stap-server
fi
exit 0

%postun server
if [ "$1" -ge "1" ] ; then
	/sbin/service stap-server condrestart >/dev/null 2>&1 || :
fi
exit 0

%post initscript
if [ $1 -eq 1 ] ; then
	/sbin/chkconfig --add systemtap
	exit 0
fi

%preun initscript
if [ $1 = 0 ] ; then
	/sbin/service systemtap stop >/dev/null 2>&1
	/sbin/chkconfig --del systemtap
fi
exit 0

%postun initscript
if [ "$1" -ge "1" ] ; then
	/sbin/service systemtap condrestart >/dev/null 2>&1 || :
fi
exit 0

%post
if [ $1 -eq 1 ] ; then
	(make -C %{_datadir}/systemtap/runtime/linux/uprobes clean) >/dev/null 3>&1 || true
	(/sbin/rmmod uprobes) >/dev/null 2>&1 || true
fi

%preun
if [ $1 -eq 0 ] ; then
	(make -C %{_datadir}/systemtap/runtime/linux/uprobes clean) >/dev/null 3>&1 || true
	(/sbin/rmmod uprobes) >/dev/null 2>&1 || true
fi

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/stap
%{_bindir}/stap-merge
%{_bindir}/stap-prep
%{_bindir}/stap-report
%{_bindir}/stapsh
%dir %{_datadir}/systemtap
%dir %{_datadir}/systemtap/runtime
%{_datadir}/systemtap/runtime/*.h
%{_datadir}/systemtap/runtime/*.c
%{_datadir}/systemtap/runtime/transport
%{_datadir}/systemtap/runtime/unwind
%dir %{_datadir}/systemtap/runtime/linux
%{_datadir}/systemtap/runtime/linux/*.c
%{_datadir}/systemtap/runtime/linux/*.h
%dir %attr(0775,root,stap-server) %{_datadir}/systemtap/runtime/linux/uprobes
%{_datadir}/systemtap/runtime/linux/uprobes/*
%dir %{_datadir}/systemtap/runtime/linux/uprobes2
%{_datadir}/systemtap/runtime/linux/uprobes2/*
%{_datadir}/systemtap/tapset
%{_mandir}/man1
%{_mandir}/man3/stap*.3stap*
%{_mandir}/man7/warning::symbols.7stap*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man8/stapsh.8*
%{_mandir}/man8/systemtap.8*
%doc AUTHORS COPYING
%{_bindir}/dtrace

%files initscript
%defattr(-,root,root)
%{_sysconfdir}/rc.d/init.d/systemtap
%dir %{_sysconfdir}/systemtap
%dir %{_sysconfdir}/systemtap/conf.d
%dir %{_sysconfdir}/systemtap/script.d
%config(noreplace) %{_sysconfdir}/systemtap/config
%dir %{_localstatedir}/cache/systemtap
%dir %{_localstatedir}/run/systemtap

%files runtime
%defattr(-,root,root)
%attr(4111,root,root) %{_bindir}/staprun
%{_libexecdir}/systemtap/stapio
%{_libexecdir}/systemtap/stap-env
%{_libexecdir}/systemtap/stap-authorize-cert
%if %with_crash
%{_libdir}/systemtap/staplog.so*
%endif
%{_mandir}/man8/staprun.8*

%files sdt-devel
%defattr(-,root,root)
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h
%doc NEWS examples

%files server
%defattr(-,root,root)
%{_bindir}/stap-server
%{_libexecdir}/systemtap/stap-serverd
%{_libexecdir}/systemtap/stap-start-server
%{_libexecdir}/systemtap/stap-stop-server
%{_libexecdir}/systemtap/stap-gen-cert
%{_libexecdir}/systemtap/stap-sign-module
%{_sysconfdir}/rc.d/init.d/stap-server
%config(noreplace) %{_sysconfdir}/logrotate.d/stap-server
%dir %{_sysconfdir}/stap-server
%dir %{_sysconfdir}/stap-server/conf.d
%config(noreplace) %{_sysconfdir}/sysconfig/stap-server
%dir %attr(0755,stap-server,stap-server) %{_localstatedir}/log/stap-server
%ghost %config %attr(0644,stap-server,stap-server) %{_localstatedir}/log/stap-server/log
%{_mandir}/man7/error::*.7stap*
%{_mandir}/man7/warning::debuginfo.7stap*
%{_mandir}/man8/stap-server.8*

%changelog
*   Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-4
-   add shadow to requires
*   Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.0-3
-   Use sqlite-{devel,libs}
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 3.0-2
-   Modified %check
*   Fri Jul 22 2016 Divya Thaluru <dthaluru@vmware.com> 3.0-1 
-   Updated version to 3.0
-   Removing patch to enable kernel (fix is present in upstream)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-5
-   GA - Bump release of all rpms
*   Mon May 23 2016 Harish Udaiya KUmar <hudaiyakumar@vmware.com> 2.9-4
-   Added the patch to enable kernel building with Kernel 4.4
*   Fri May 20 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9-3 
-   Fixed the stap-prep script to be compatible with Photon
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-2
-   Fix for upgrade issues
*   Wed Dec 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9-1 
-   Updated version to 2.9
*   Fri Dec 11 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7-2
-   Move dtrace to the main package.
*   Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 2.7-1
-   Initial build. First version
