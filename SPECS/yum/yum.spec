Summary:        RPM installer/updater
Name:           yum
Version:        3.4.3
Release:        10%{?dist}
License:        GPLv2+
Group:          System Environment/Base
Source0:        %{name}-%{version}.tar.gz
Patch0:         yumconf.patch
Patch1:         parser.patch
Patch2:         yum-repo-name.patch
Patch3:         yum-CVE-2013-1910.patch
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
BuildArchitectures: noarch

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded
automatically, prompting the user for permission as necessary.

%prep
%autosetup -p1

%build
make %{?_smp_mflags}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install %{?_smp_mflags}

# Ghost files:
mkdir -p %{buildroot}/var/lib/yum/history
mkdir -p %{buildroot}/var/lib/yum/plugins
mkdir -p %{buildroot}/var/lib/yum/yumdb
touch %{buildroot}/var/lib/yum/uuid

%find_lang %name

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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

%exclude %{_sysconfdir}/cron.daily/0yum.cron
%exclude %config(noreplace) %{_sysconfdir}/yum/yum-daily.yum
%exclude %config(noreplace) %{_sysconfdir}/yum/yum-weekly.yum
%exclude %{_sysconfdir}/rc.d/init.d/yum-cron
%exclude %config(noreplace) %{_sysconfdir}/sysconfig/yum-cron

%exclude %config(noreplace) %{_sysconfdir}/yum/yum-updatesd.conf
%exclude %config %{_sysconfdir}/rc.d/init.d/yum-updatesd
%exclude %config %{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
%exclude %{_datadir}/yum-cli/yumupd.py*
%exclude %{_sbindir}/yum-updatesd
%exclude %{_mandir}/man*/yum-updatesd*

%changelog
*   Tue Jun 01 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.4.3-10
-   Bump version as a part of rpm upgrade
*   Tue Nov 12 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.4.3-9
-   Fix CVE-2013-1910
*   Wed Aug 23 2017 Xiaolin Li <xiaolinl@vmware.com> 3.4.3-8
-   Replaced variables in repo name.
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
