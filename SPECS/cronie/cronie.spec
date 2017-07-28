Summary:        Cron Daemon
Name:           cronie
Version:        1.5.0
Release:        12%{?dist}
License:        GPLv2+ and MIT and BSD and ISC
URL:            https://fedorahosted.org/cronie
Source0:        https://fedorahosted.org/releases/c/r/cronie/%{name}-%{version}.tar.gz
%define sha1 cronie=bbf154a6db7c9802664d1f0397b5e7ae9a9618e4
Source1:        run-parts.sh
Patch0:         cronie_fix_pam_configuration.patch
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libselinux-devel
BuildRequires:  Linux-PAM
BuildRequires:  systemd
Requires:       systemd
Requires:       libselinux
Requires:       Linux-PAM
%description
Cronie contains the standard UNIX daemon crond that runs specified programs at
scheduled times and related tools. It is based on the original cron and
has security and configuration enhancements like the ability to use pam and
SELinux.
%prep
%setup -q
sed -i "s/\/usr\/sbin\/anacron -s/\/usr\/sbin\/anacron -s -S \/var\/spool\/anacron/" contrib/0anacron
%patch0 -p1
%build
autoreconf
./configure \
	--prefix=%{_prefix} \
        --sysconfdir=/etc   \
	--with-pam	    \
	--with-selinux      \
	--enable-anacron    \
	--enable-pie        \
	--enable-relro
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm700 %{buildroot}/usr/var/spool/cron
install -vd %{buildroot}%{_sysconfdir}/sysconfig/
install -vd %{buildroot}%{_sysconfdir}/cron.d/
install -vd %{buildroot}%{_sysconfdir}/cron.hourly
install -vd %{buildroot}%{_sysconfdir}/cron.daily
install -vd %{buildroot}%{_sysconfdir}/cron.weekly
install -vd %{buildroot}%{_sysconfdir}/cron.monthly
install -vd %{buildroot}/var/spool/anacron

install -m 644 crond.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/crond
install -m 644 contrib/anacrontab %{buildroot}%{_sysconfdir}/anacrontab
install -c -m644 contrib/0hourly %{buildroot}%{_sysconfdir}/cron.d/0hourly
install -c -m755 contrib/0anacron %{buildroot}%{_sysconfdir}/cron.hourly/0anacron
install -m 644 contrib/dailyjobs %{buildroot}%{_sysconfdir}/cron.d/dailyjobs

touch %{buildroot}%{_sysconfdir}/cron.deny
touch %{buildroot}/var/spool/anacron/cron.daily
touch %{buildroot}/var/spool/anacron/cron.weekly
touch %{buildroot}/var/spool/anacron/cron.monthly

install -vdm755 %{buildroot}/%{_sysconfdir}/pam.d
install -vd %{buildroot}%{_libdir}/systemd/system/
install -m 644 contrib/cronie.systemd %{buildroot}%{_libdir}/systemd/system/crond.service
sed -i 's/ypbind.service//g' %{buildroot}%{_libdir}/systemd/system/crond.service
install -c -m755  %{SOURCE1} %{buildroot}/%{_bindir}/run-parts

ln -sfv ./crond.service %{buildroot}/usr/lib/systemd/system/cron.service

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
/sbin/ldconfig
%systemd_post crond.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart crond.service

%preun
%systemd_preun crond.service

%files
%defattr(-,root,root)
%{_lib}/systemd/system/cron.service
%config(noreplace) %{_sysconfdir}/pam.d/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir /usr/var/spool/cron
%dir %{_sysconfdir}/sysconfig/
%dir %{_sysconfdir}/cron.d/
%dir %{_sysconfdir}/cron.hourly
%dir %{_sysconfdir}/cron.daily
%dir %{_sysconfdir}/cron.weekly
%dir %{_sysconfdir}/cron.monthly
%config(noreplace) %{_sysconfdir}/anacrontab
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/*
%config(noreplace) %{_sysconfdir}/cron.deny
%{_sysconfdir}/cron.hourly/0anacron
%config(noreplace) %{_sysconfdir}/sysconfig/crond
%{_libdir}/systemd/system/crond.service
/var/spool/anacron/cron.daily
/var/spool/anacron/cron.monthly
/var/spool/anacron/cron.weekly
%changelog
*   Fri Jul 28 2017 Dheerajs Shetty <dheerajs@vmware.com>  1.5.0-12
-   Remove ypbind.service from crond.service file
*   Mon Aug 29 2016 Divya Thaluru <dthaluru@vmware.com>  1.5.0-11
-   Fixed pam configuration for crond
*   Thu Aug 4 2016 Divya Thaluru <dthaluru@vmware.com>  1.5.0-10
-   Added logic to not replace conf files in upgrade scenario
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.0-9
-   GA - Bump release of all rpms
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  1.5.0-8
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Thu Mar 24 2016 Xiaolin Li <xiaolinl@vmware.com>  1.5.0-7
-   Add run-parts command.
*   Fri Mar 04 2016 Anish Swaminathan <anishs@vmware.com>  1.5.0-6
-   Add folders to sysconfdir.
*   Mon Feb 08 2016 Anish Swaminathan <anishs@vmware.com>  1.5.0-5
-   Change default sysconfdir.
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.5.0-4
-   Add systemd to Requires and BuildRequires.
-   Use systemctl to enable/disable service.
*   Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 1.5.0-3
-   Symlink cron.service to crond.service.
-   And move the /usr/etc/pam.d/crond to /etc/pam.d/crond
*   Thu Nov 12 2015 Xiaolin Li <xiaolinl@vmware.com> 1.5.0-2
-   Add crond to systemd service.
*   Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
-   Initial build. First version

