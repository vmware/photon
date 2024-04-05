Summary:        The Apache HTTP Server
Name:           httpd
Version:        2.4.59
Release:        1%{?dist}
License:        Apache License 2.0
URL:            http://httpd.apache.org/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://dlcdn.apache.org/%{name}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=209da0bbac5e2564d4590302515b35495be6402273ff4024aa93e85e44554c95e053201d606383936425a41e1b5b97e6b40055dcbb385eb691a5029a6f3158c2

# Patch0 is taken from:
# https://www.linuxfromscratch.org/patches/blfs/svn
Patch0: %{name}-%{version}-blfs_layout-1.patch
Patch1: %{name}-uncomment-ServerName.patch

BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: apr
BuildRequires: apr-util
BuildRequires: apr-util-devel
BuildRequires: openldap
BuildRequires: expat-devel
BuildRequires: lua-devel
BuildRequires: nghttp2-devel

Requires: nghttp2
Requires: pcre
Requires: apr-util
Requires: openssl
Requires: openldap
Requires: lua
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

Provides: apache2

%define _confdir %{_sysconfdir}

%description
The Apache HTTP Server.

%package devel
Summary:    Header files for httpd
Group:      Applications/System
Requires:   %{name}

%description devel
These are the header files of httpd.

%package docs
Summary:    Help files for httpd
Group:      Applications/System
Requires:   %{name}

%description docs
These are the help files of httpd.

%package tools
Group:      System Environment/Daemons
Summary:    Tools for httpd

%description tools
The httpd-tools of httpd.

%prep
%autosetup -p1

%build
sh ./configure \
            --host=%{_host} \
            --build=%{_host} \
            --prefix="%{_sysconfdir}/%{name}" \
            --exec-prefix="%{_prefix}" \
            --libdir=%{_libdir} \
            --bindir="%{_bindir}" \
            --sbindir="%{_sbindir}" \
            --sysconfdir="%{_confdir}/%{name}/conf" \
            --libexecdir="%{_libdir}/%{name}/modules" \
            --datadir="%{_sysconfdir}/%{name}" \
            --includedir="%{_includedir}" \
            --mandir="%{_mandir}" \
            --enable-authnz-fcgi \
            --enable-mods-shared="all cgi" \
            --enable-mpms-shared=all \
            --with-apr=%{_prefix} \
            --with-apr-util=%{_prefix} \
            --enable-layout=RPM \
            --enable-http2

make %{?_smp_mflags}

%install
# make doesn't support _smp_mflags
make DESTDIR=%{buildroot} install

install -vdm755 %{buildroot}%{_unitdir}
cat << EOF >> %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/var/run/%{name}/%{name}.pid
ExecStart=%{_sbindir}/%{name} -k start
ExecStop=%{_sbindir}/%{name} -k stop
ExecReload=%{_sbindir}/%{name} -k graceful

[Install]
WantedBy=multi-user.target
EOF

install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

ln -sfv %{_sbindir}/%{name} %{buildroot}%{_sbindir}/apache2
ln -sfv /etc/%{name}/conf/%{name}.conf %{buildroot}/etc/%{name}/%{name}.conf

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{name}.conf << EOF
d /var/run/%{name} 0755 root root -
EOF

%post
/sbin/ldconfig
if [ $1 -eq 1 ]; then
  # this is initial installation
  if ! getent group apache >/dev/null; then
    groupadd -g 25 apache
  fi

  if ! getent passwd apache >/dev/null; then
    useradd -c "Apache Server" -d /srv/www -g apache -s /bin/false -u 25 apache
  fi

  if [ -h /etc/mime.types ]; then
    mv /etc/mime.types /etc/mime.types.orig
  fi
fi

ln -sfv /etc/%{name}/conf/mime.types /etc/mime.types
systemd-tmpfiles --create %{name}.conf
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  # this is delete operation
  if getent passwd apache >/dev/null; then
    userdel apache
  fi
  if getent group apache >/dev/null; then
    groupdel apache
  fi

  if [ -f /etc/mime.types.orig ]; then
    mv /etc/mime.types.orig /etc/mime.types
  fi
fi
%systemd_postun_with_restart %{name}.service

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files docs
%defattr(-,root,root)
%{_sysconfdir}/%{name}/manual/*

%files
%defattr(-,root,root)
%{_libdir}/%{name}/*
%{_bindir}/*
%exclude %{_bindir}/apxs
%exclude %{_bindir}/dbmmanage
%{_sbindir}/*
%{_datadir}/*
%{_sysconfdir}/%{name}/html/index.html
%{_sysconfdir}/%{name}/cgi-bin/*
%{_sysconfdir}/%{name}/conf/extra
%{_sysconfdir}/%{name}/conf/original
%config(noreplace) %{_sysconfdir}/%{name}/conf/magic
%{_sysconfdir}/%{name}/conf/envvars
%config(noreplace) %{_sysconfdir}/%{name}/conf/%{name}.conf
%{_sysconfdir}/%{name}/conf/mime.types
%{_sysconfdir}/%{name}/error/*
%{_sysconfdir}/%{name}/icons/*
%{_sysconfdir}/%{name}/%{name}.conf
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%{_tmpfilesdir}/%{name}.conf
%{_localstatedir}/log/%{name}

%files tools
%defattr(-,root,root)
%{_bindir}/apxs
%{_bindir}/dbmmanage

%changelog
* Fri Apr 05 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.4.59-1
- Version upgrade to v2.4.59 to fix CVE-2024-27316
* Mon Oct 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.4.58-1
- Version upgrade to v2.4.58 to fix CVE-2023-31122
* Mon Oct 23 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.4.56-2
- Version bump as part of nghtttp2 upgrade
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 2.4.56-1
- Upgrade to v2.4.56 to fix following CVE's:
- CVE-2023-25690, and CVE-2023-27522
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.4.55-1
- Upgrade to v2.4.55 to fix following CVE's:
- CVE-2006-20001, CVE-2022-37436, and CVE-2022-36760
* Mon Jun 20 2022 Nitesh Kumar <kunitesh@vmware.com> 2.4.54-1
- Upgrade to v2.4.54 to fix bunch of CVEs
* Mon Mar 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.4.53-1
- Upgrade to v2.4.53 to fix bunch of CVEs
* Thu Dec 23 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.52-1
- Upgrade to v2.4.52 to fix CVE-2021-44790
* Mon Nov 08 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.51-2
- Enable mod_http2
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.51-1
- Version upgrade to fix CVE-2021-42013
* Tue Oct 05 2021 Dweep Advani <dadvani@vmware.com> 2.4.48-4
- Patched for CVE-2021-39275
* Wed Sep 29 2021 Dweep Advani <dadvani@vmware.com> 2.4.48-3
- Patched for CVE-2021-34798, CVE-2021-36160 and CVE-2021-40438
* Mon Sep 13 2021 Dweep Advani <dadvani@vmware.com> 2.4.48-2
- Patched for CVE-2021-33193
* Mon Jun 21 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.48-1
- Update httpd to 2.4.48 to fix CVE-2020-35452, CVE-2020-13950
- CVE-2019-17567
* Mon Aug 10 2020 Dweep Advani <dadvani@vmware.com> 2.4.46-1
- Upgraded to version 2.4.46 for addressing CVEs
* Wed Apr 08 2020 Dweep Advani <dadvani@vmware.com> 2.4.43-2
- Fixed failed httpd service startup issue on reboots
* Mon Apr 06 2020 Shreyas B. <shreyasb@vmware.com> 2.4.43-1
- Upgrading to 2.4.43 to address following CVEs.
- (1) CVE-2020-1927 (2) CVE-2020-1934
* Mon Sep 30 2019 Shreyas B. <shreyasb@vmware.com> 2.4.41-1
- Upgrading to 2.4.41 to address following CVEs.
- (1) CVE-2019-10092 (2) CVE-2019-10098 (3) CVE-2019-10082
- (4) CVE-2019-10081 (5) CVE-2019-9517
* Thu Apr 25 2019 Dweep Advani <dadvani@vmware.com> 2.4.39-1
- Upgrading to 2.4.39 for fixing multiple CVEs
- (1) CVE-2018-17189 (2) CVE-2018-17199 (3) CVE-2019-0190
- (4) CVE-2019-0211 (5) CVE-2019-0215 (6) CVE-2019-0217
* Wed Mar 13 2019 Michelle Wang <michellew@vmware.com> 2.4.34-4
- Fix configure for rel_libexecdir variable with RPMS layout
* Thu Mar 7 2019 Michelle Wang <michellew@vmware.com> 2.4.34-3
- Update build configure for httpd to use RPM layout
* Thu Jan 24 2019 Dweep Advani <dadvani@vmware.com> 2.4.34-2
- Fixed CVE-2018-11763
* Wed Aug 29 2018 Tapas Kundu <tkundu@vmware.com> 2.4.34-1
- Updated to version 2.4.34, fix CVE-2018-1333
* Mon Oct 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.28-1
- Updated to version 2.4.28
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.27-3
- Remove shadow from requires and use explicit tools for post actions
* Mon Aug 07 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-2
- Add shadow to requires for useradd/groupadd
* Mon Jul 24 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-1
- Updated to version 2.4.27 - Fixes CVE-2017-3167
* Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.4.25-3
- Provide preset file to disable service by default.
* Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-2
- Fixing httpd.pid file write issue
* Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-1
- Updated to version 2.4.25
* Tue Dec 27 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.18-8
- BuildRequires lua, Requires lua.
* Wed Dec 21 2016 Anish Swaminathan <anishs@vmware.com>  2.4.18-7
- Change config file properties for httpd.conf
* Thu Jul 28 2016 Divya Thaluru <dthaluru@vmware.com> 2.4.18-6
- Removed packaging of debug files
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 2.4.18-5
- Added patch for CVE-2016-5387
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.18-4
- GA - Bump release of all rpms
* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.4.18-3
- Adding upgrade support in pre/post/un script.
* Mon Mar 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.18-2
- Fixing systemd service
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.18-1
- Updated to version 2.4.18
* Mon Nov 23 2015 Sharath George <sharathg@vmware.com> 2.4.12-4
- Add /etc/mime.types
* Tue Sep 29 2015 Xiaolin Li <xiaolinl@vmware.com> 2.4.12-3
- Move perl script to tools package.
* Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-2
- Added service file. Changed installation paths.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-1
- Initial build. First version
