Summary:	Cron Daemon
Name:		cronie
Version:	1.5.0
Release:	1%{?dist}
License:	GPLv2+ and MIT and BSD and ISC
URL:		https://fedorahosted.org/cronie
Source0:	https://fedorahosted.org/releases/c/r/cronie/%{name}-%{version}.tar.gz
%define sha1 cronie=bbf154a6db7c9802664d1f0397b5e7ae9a9618e4
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	libselinux-devel
BuildRequires:	Linux-PAM
Requires:	libselinux
Requires:	Linux-PAM
%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is based on the original cron and
has security and configuration enhancements like the ability to use pam and
SELinux.
%prep
%setup -q
%build
autoreconf
./configure \
	--prefix=%{_prefix} \
	--with-pam	\
	--with-selinux \
	--enable-anacron \
	--enable-pie \
	--enable-relro
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm700 %{buildroot}/usr/var/spool/cron
install -vd %{buildroot}%{_sysconfdir}/sysconfig/
install -vd %{buildroot}%{_sysconfdir}/cron.d/
install -vd %{buildroot}%{_sysconfdir}/cron.hourly
install -vd %{buildroot}/var/spool/anacron

install -m 644 crond.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/crond
install -m 644 contrib/anacrontab %{buildroot}%{_sysconfdir}/anacrontab
install -c -m755 contrib/0hourly %{buildroot}%{_sysconfdir}/cron.d/0hourly
install -c -m755 contrib/0anacron %{buildroot}%{_sysconfdir}/cron.hourly/0anacron
install -m 644 contrib/dailyjobs %{buildroot}%{_sysconfdir}/cron.d/dailyjobs

touch %{buildroot}%{_sysconfdir}/cron.deny
touch %{buildroot}/var/spool/anacron/cron.daily
touch %{buildroot}/var/spool/anacron/cron.weekly
touch %{buildroot}/var/spool/anacron/cron.monthly

install -vd %{buildroot}%{_libdir}/systemd/system/
install -m 644 contrib/cronie.systemd %{buildroot}%{_libdir}/systemd/system/crond.service

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
/usr/etc/pam.d/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir /usr/var/spool/cron
%dir %{_sysconfdir}/sysconfig/
%dir %{_sysconfdir}/cron.d/
%dir %{_sysconfdir}/cron.hourly
%{_sysconfdir}/anacrontab
%{_sysconfdir}/cron.d/*
%{_sysconfdir}/cron.deny
%{_sysconfdir}/cron.hourly/0anacron
%{_sysconfdir}/sysconfig/crond
%{_libdir}/systemd/system/crond.service
/var/spool/anacron/cron.daily
/var/spool/anacron/cron.monthly
/var/spool/anacron/cron.weekly
%changelog
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
-	Initial build. First version

