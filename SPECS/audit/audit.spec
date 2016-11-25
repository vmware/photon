Summary:	Kernel Audit Tool
Name:		audit
Version:	2.5
Release:	6%{?dist}
Source0:	http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
%define sha1 audit=b684a8dca31776a4184044733cd5fd4b1b652298
License:	GPLv2+
Group:		System Environment/Security
URL:		http://people.redhat.com/sgrubb/audit/
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildRequires:	krb5-devel
BuildRequires:	openldap
BuildRequires:	go
BuildRequires:	tcp_wrappers-devel
BuildRequires:	libcap-ng-devel
BuildRequires:	swig
BuildRequires:  e2fsprogs-devel
BuildRequires:  systemd
Requires:	systemd
Requires:	krb5
Requires:	openldap
Requires:	python2
Requires:	tcp_wrappers
Requires:	libcap-ng
Requires:   gawk

%description
The audit package contains the user space utilities for
storing and searching the audit records generate by
the audit subsystem in the Linux 2.6 kernel.

%package devel
Summary:	The libraries and header files needed for audit development.
Requires: 	%{name} = %{version}-%{release}

%description devel
The libraries and header files needed for audit development.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--exec_prefix=/usr \
	--sbindir=%{_sbindir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--with-python=yes \
	--without-python3 \
        --with-libwrap \
	--enable-gssapi-krb5=yes \
        --with-libcap-ng=yes \
	--with-aarch64 \
        --enable-zos-remote \
	--with-golang \
	--enable-systemd

make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/{etc/audispd/plugins.d,etc/audit/rules.d}
mkdir -p %{buildroot}/%{_var}/log/audit
mkdir -p %{buildroot}/%{_var}/spool/audit
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post  auditd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart auditd.service

%preun
%systemd_preun auditd.service

%files 
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/python*/*
%{_libdir}/golang/*
%{_libdir}/systemd/system/auditd.service
%{_libexecdir}/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_var}/log/audit
%{_var}/spool/audit
%attr(750,root,root) %dir %{_sysconfdir}/audit
%attr(750,root,root) %dir %{_sysconfdir}/audit/rules.d
%attr(750,root,root) %dir %{_sysconfdir}/audisp
%attr(750,root,root) %dir %{_sysconfdir}/audisp/plugins.d
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/auditd.conf
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/rules.d/audit.rules
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audit.rules
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/audispd.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/plugins.d/af_unix.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/plugins.d/syslog.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/plugins.d/audispd-zos-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/zos-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/audisp-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/plugins.d/au-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/libaudit.conf
/usr/share/aclocal/audit.m4

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h

%changelog
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.5-6
- Required krb5-devel.
* Fri Jul 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-5
- Add gawk requirement.
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-4
- Fixed logic to restart the active services after upgrade 
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-3
- GA - Bump release of all rpms
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-2
- Fixing spec file to handle rpm upgrade scenario correctly
* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  2.5-1
- Upgrade to 2.5
* Fri Jan 29 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-4
- Add directories for auditd service.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-3
- Change config file attributes.
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 2.4.4-2
- Add systemd requirement.
* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.4.4-1
- Initial version
