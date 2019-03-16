Summary:        RPM installer/updater
Name:           yum
Version:        3.4.3
Release:        8%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Source0:        %{name}-%{version}.tar.gz
Patch0:         yumconf.patch
Patch1:         parser.patch
%define sha1    yum=8ec5d339e4518a7908fd4db0721740288a3d8b6c
URL:            http://yum.baseurl.org/
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  pycurl
BuildRequires:  urlgrabber
Requires:       python2
Requires:       python2-libs
Requires:       python-xml
Requires:       urlgrabber
Requires:       yum-metadata-parser >= 1.1.0
Requires:       pycurl
Requires:       rpm-devel
Requires:       python-rpm
Conflicts:      rpm >= 5-0
Obsoletes:      yum-skip-broken <= 1.1.18
Obsoletes:      yum-basearchonly <= 1.1.9
Obsoletes:      yum-allow-downgrade < 1.1.20-0
Obsoletes:      yum-plugin-allow-downgrade < 1.1.22-0
Obsoletes:      yum-plugin-protect-packages < 1.1.27-0
Provides:       yum-skip-broken
Provides:       yum-basearchonly
Provides:       yum-allow-downgrade
Provides:       yum-plugin-allow-downgrade
Provides:       yum-protect-packages
Provides:       yum-plugin-protect-packages
BuildArch:      noarch

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded
automatically, prompting the user for permission as necessary.

# %package updatesd
# Summary: Update notification daemon
# Group: Applications/System
# Requires: yum = %{version}-%{release}
# Requires: dbus-python
# Requires(preun): /sbin/chkconfig
# Requires(preun): /sbin/service
# Requires(postun): /sbin/chkconfig
# Requires(postun): /sbin/service


# %description updatesd
# yum-updatesd provides a daemon which checks for available updates and
# can notify you when they are available via email, syslog or dbus.


# %package cron
# Summary: Files needed to run yum updates as a cron job
# Group: System Environment/Base
# # Requires: yum >= 3.0 vixie-cron crontabs yum-plugin-downloadonly findutils
# Requires(post): /sbin/chkconfig
# Requires(post): /sbin/service
# Requires(preun): /sbin/chkconfig
# Requires(preun): /sbin/service
# Requires(postun): /sbin/service

# %description cron
# These are the files needed to run yum updates as a cron job.
# Install this package if you want auto yum updates nightly via cron.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/yum/yum.conf
# install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/yum.cron

# Ghost files:
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/history
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/plugins
mkdir -p $RPM_BUILD_ROOT/var/lib/yum/yumdb
touch $RPM_BUILD_ROOT/var/lib/yum/uuid

%find_lang %name

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


# %post updatesd
# /sbin/chkconfig --add yum-updatesd
# /sbin/service yum-updatesd condrestart >/dev/null 2>&1
# exit 0

# %preun updatesd
# if [ $1 = 0 ]; then
#  /sbin/chkconfig --del yum-updatesd
#  /sbin/service yum-updatesd stop >/dev/null 2>&1
# fi
# exit 0


# %post cron
# # Make sure chkconfig knows about the service
# /sbin/chkconfig --add yum-cron
# # if an upgrade:
# if [ "$1" -ge "1" ]; then
# # if there's a /etc/rc.d/init.d/yum file left, assume that there was an
# # older instance of yum-cron which used this naming convention.  Clean
# # it up, do a conditional restart
#  if [ -f /etc/init.d/yum ]; then
# # was it on?
#   /sbin/chkconfig yum
#   RETVAL=$?
#   if [ $RETVAL = 0 ]; then
# # if it was, stop it, then turn on new yum-cron
#    /sbin/service yum stop 1> /dev/null 2>&1
#    /sbin/service yum-cron start 1> /dev/null 2>&1
#    /sbin/chkconfig yum-cron on
#   fi
# # remove it from the service list
#   /sbin/chkconfig --del yum
#  fi
# fi
# exit 0

# %preun cron
# # if this will be a complete removeal of yum-cron rather than an upgrade,
# # remove the service from chkconfig control
# if [ $1 = 0 ]; then
#  /sbin/chkconfig --del yum-cron
#  /sbin/service yum-cron stop 1> /dev/null 2>&1
# fi
# exit 0
#
# %postun cron
# # If there's a yum-cron package left after uninstalling one, do a
# # conditional restart of the service
# if [ "$1" -ge "1" ]; then
#  /sbin/service yum-cron condrestart 1> /dev/null 2>&1
# fi
# exit 0

%files -f %{name}.lang
%defattr(-, root, root)
%doc README AUTHORS COPYING TODO INSTALL ChangeLog PLUGINS
%config(noreplace) %{_sysconfdir}/yum/yum.conf
%config(noreplace) %{_sysconfdir}/yum/version-groups.conf
%dir %{_sysconfdir}/yum
%dir %{_sysconfdir}/yum/protected.d
%dir %{_sysconfdir}/yum/repos.d
%dir %{_sysconfdir}/yum/vars
%config %{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/bash_completion.d
%{_datadir}/yum-cli/*
%exclude %{_datadir}/yum-cli/yumupd.py*
%{_bindir}/yum
/usr/lib/python?.?/site-packages/yum
/usr/lib/python?.?/site-packages/rpmUtils
%dir /var/cache/yum
%dir /var/lib/yum
%ghost /var/lib/yum/uuid
%ghost /var/lib/yum/history
%ghost /var/lib/yum/plugins
%ghost /var/lib/yum/yumdb
%{_mandir}/man*/yum.*
%{_mandir}/man*/yum-shell*

#excluding cron and updatesd for now.

#%files cron
#%defattr(-,root,root)
%exclude %{_sysconfdir}/cron.daily/0yum.cron
%exclude %config(noreplace) %{_sysconfdir}/yum/yum-daily.yum
%exclude %config(noreplace) %{_sysconfdir}/yum/yum-weekly.yum
%exclude %{_sysconfdir}/rc.d/init.d/yum-cron
%exclude %config(noreplace) %{_sysconfdir}/sysconfig/yum-cron

#%files updatesd
#%defattr(-, root, root)
%exclude %config(noreplace) %{_sysconfdir}/yum/yum-updatesd.conf
%exclude %config %{_sysconfdir}/rc.d/init.d/yum-updatesd
%exclude %config %{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
%exclude %{_datadir}/yum-cli/yumupd.py*
%exclude %{_sbindir}/yum-updatesd
%exclude %{_mandir}/man*/yum-updatesd*

%changelog
*   Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 3.4.3-8
-   Replaced BuildArchitecture to BuildArch
*   Wed Mar 29 2017 Xiaolin Li <xiaolinl@vmware.com> 3.4.3-7
-   Added python-rpm to requires.
*   Mon Jun 06 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.3-6
-   Engage missing patches for yum config and parser
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.3-5
-   GA - Bump release of all rpms
*   Wed May 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.3-4
-   Fix to read photon repo files, set distroverpkg to photon-release
*   Thu Apr 28 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.3-3
-   Add python-xml dependency
*   Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 3.4.3-2
-   Adding python and python-libs as run time dependent packages
