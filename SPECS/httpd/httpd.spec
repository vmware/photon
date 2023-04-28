Summary:        The Apache HTTP Server
Name:           httpd
Version:        2.4.56
Release:        1%{?dist}
License:        Apache License 2.0
URL:            http://httpd.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://dlcdn.apache.org/%{name}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=5f12cd9878d822384b1bb163fea4d8edee5e7a0dd8b2389264387971268145cccc6a5a27ddf0436c5f1f631acc5fdc4874da2a47911483e421ca40bf783e0e12
Source1: %{name}.sysusers

# Patch0 is taken from:
# https://www.linuxfromscratch.org/patches/blfs/svn
Patch0: %{name}-%{version}-blfs_layout-1.patch
Patch1: %{name}-uncomment-ServerName.patch

BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  apr
BuildRequires:  apr-util-devel
BuildRequires:  openldap-devel
BuildRequires:  expat-devel
BuildRequires:  lua-devel
BuildRequires:  nghttp2-devel
BuildRequires:  systemd-devel

Requires:       nghttp2
Requires:       pcre
Requires:       apr-util
Requires:       openssl
Requires:       openldap
Requires:       lua
Requires(pre):  systemd-rpm-macros
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

Provides:       apache2

%description
The Apache HTTP Server.

%package devel
Summary:  Header files for httpd
Group:    Applications/System
Requires: %{name} = %{version}-%{release}

%description devel
These are the header files of httpd.

%package docs
Summary:  Help files for httpd
Group:    Applications/System
Requires: %{name} = %{version}-%{release}

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
sh ./configure --host=%{_host} --build=%{_build} \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --program-prefix= \
    --disable-dependency-tracking \
    --prefix=%{_sysconfdir}/%{name} \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir}/%{name}/conf \
    --datadir=%{_sysconfdir}/%{name} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir}/%{name}/modules \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-authnz-fcgi \
    --enable-mods-shared="all cgi" \
    --enable-mpms-shared=all \
    --with-apr=%{_prefix} \
    --with-apr-util=%{_prefix} \
    --enable-layout=RPM \
    --enable-http2

$(dirname $(gcc -print-prog-name=cc1))/install-tools/mkheaders

%make_build

%install
%make_install %{?_smp_mflags}

install -vdm755 %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_sysconfdir}/%{name}/logs
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

cat << EOF >> %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/run/%{name}/%{name}.pid
ExecStart=%{_sbindir}/%{name} -k start
ExecStop=%{_sbindir}/%{name} -k stop
ExecReload=%{_sbindir}/%{name} -k graceful

[Install]
WantedBy=multi-user.target
EOF

install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

ln -sfrv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/apache2
ln -sfrv %{buildroot}%{_sysconfdir}/%{name}/conf/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{name}.conf << EOF
d /run/%{name} 0755 root root -
EOF

%post
/sbin/ldconfig
if [ $1 -eq 1 ]; then
  # this is initial installation
  %sysusers_create_compat %{SOURCE1}

  if [ -h %{_sysconfdir}/mime.types ]; then
    mv %{_sysconfdir}/mime.types %{_sysconfdir}/mime.types.orig
  fi
fi

ln -sfr %{_sysconfdir}/%{name}/conf/mime.types %{_sysconfdir}/mime.types
systemd-tmpfiles --create %{name}.conf
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  if [ -f %{_sysconfdir}/mime.types.orig ]; then
    mv %{_sysconfdir}/mime.types.orig %{_sysconfdir}/mime.types
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
%{_sysusersdir}/%{name}.sysusers

%files tools
%defattr(-,root,root)
%{_bindir}/apxs
%{_bindir}/dbmmanage

%changelog
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 2.4.56-1
- Upgrade to v2.4.56 to fix following CVE's:
- CVE-2023-25690, and CVE-2023-27522
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 2.4.55-3
- Use systemd-rpm-macros for user creation
* Wed Feb 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.55-2
- Bump version as a part of openldap upgrade
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.4.55-1
- Upgrade to v2.4.55 to fix following CVE's:
- CVE-2006-20001, CVE-2022-37436, and CVE-2022-36760
* Mon Jun 20 2022 Nitesh Kumar <kunitesh@vmware.com> 2.4.54-1
- Upgrade to v2.4.54 to fix bunch of CVEs
* Mon Mar 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.4.53-1
- Upgrade to v2.4.53 to fix bunch of CVEs
* Thu Dec 23 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.52-1
- Upgrade to v2.4.52 to fix CVE-2021-44790
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.51-3
- Bump up release for openssl
* Mon Nov 08 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.51-2
- Enable mod_http2
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.51-1
- Version upgrade to fix CVE-2021-42013
* Thu Oct 07 2021 Dweep Advani <dadvani@vmware.com> 2.4.50-1
- Upgraded to 2.4.50 for fixing CVE-2021-41524 and CVE-2021-41773
* Tue Oct 05 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.49-1
- Upgraded to 2.4.49 for addressing multiple CVEs
* Fri May 21 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.47-1
- Upgrade to version 2.4.47
* Wed Jan 20 2021 Tapas Kundu <tkundu@vmware.com> 2.4.46-5
- Fix pid path
* Fri Oct 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.4.46-4
- Fix GCC path issue
* Mon Oct 05 2020 Dweep Advani <dadvani@vmware.com> 2.4.46-3
- Create /var/run/httpd temp folder through systemd-tmpfiles
* Tue Sep 01 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.46-2
- Make openssl 1.1.1 compatible
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.46-1
- Automatic Version Bump
* Mon Sep 30 2019 Shreyas B. <shreyasb@vmware.com> 2.4.41-1
- Upgrading to 2.4.41 to address following CVEs.
- (1) CVE-2019-10092 (2) CVE-2019-10098 (3) CVE-2019-10082
- (4) CVE-2019-10081 (5) CVE-2019-9517
* Tue Apr 16 2019 Dweep Advani <dadvani@vmware.com> 2.4.39-1
- Upgrading to 2.4.39 for fixing multiple CVEs
- (1) CVE-2018-17189 (2) CVE-2018-17199 (3) CVE-2019-0190
- (4) CVE-2019-0211 (5) CVE-2019-0215 (6) CVE-2019-0217
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
- Provide preset file to deactivate service by default.
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
