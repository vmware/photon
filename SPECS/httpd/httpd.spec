Summary:        The Apache HTTP Server
Name:           httpd
Version:        2.4.39
Release:        1%{?dist}
License:        Apache License 2.0
URL:            http://httpd.apache.org/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://apache.mirrors.hoobly.com/%{name}/%{name}-%{version}.tar.bz2
%define sha1    httpd=75695bb7bb589c308755bf496de8b34522133865
Patch0:         http://www.linuxfromscratch.org/patches/blfs/svn/%{name}-%{version}-blfs_layout-1.patch
Patch1:         httpd-uncomment-ServerName.patch
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  apr
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  openldap
BuildRequires:  expat
BuildRequires:  lua-devel
Requires:       pcre
Requires:       apr-util
Requires:       openssl
Requires:       openldap
Requires:       lua
Requires:       shadow
Provides:       apache2
%description
The Apache HTTP Server.

%package devel
Summary: Header files for httpd
Group: Applications/System
Requires: httpd
%description devel
These are the header files of httpd.

%package docs
Summary: Help files for httpd
Group: Applications/System
Requires: httpd
%description docs
These are the help files of httpd.

%package tools
Group: System Environment/Daemons
Summary: Tools for httpd

%description tools
The httpd-tools of httpd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./configure --prefix=%{_sysconfdir}/httpd \
            --exec-prefix=%{_prefix} \
            --bindir=%{_bindir}                             \
            --sbindir=%{_sbindir}                           \
            --mandir=%{_mandir}                             \
            --libdir=%{_libdir}                             \
            --sysconfdir=%{_sysconfdir}/httpd/conf          \
            --includedir=%{_includedir}/httpd               \
            --libexecdir=%{_libdir}/httpd/modules           \
            --enable-authnz-fcgi                            \
            --enable-mods-shared="all cgi"                  \
            --enable-mpms-shared=all                        \
            --with-apr=%{_prefix}                           \
            --with-apr-util=%{_prefix}

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -vdm755 %{buildroot}/usr/lib/systemd/system
install -vdm755 %{buildroot}/etc/httpd/logs

cat << EOF >> %{buildroot}/usr/lib/systemd/system/httpd.service
[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/var/run/httpd/httpd.pid
ExecStart=/usr/sbin/httpd -k start
ExecStop=/usr/sbin/httpd -k stop
ExecReload=/usr/sbin/httpd -k graceful

[Install]
WantedBy=multi-user.target

EOF
ln -s /usr/sbin/httpd %{buildroot}/usr/sbin/apache2
ln -s /etc/httpd/conf/httpd.conf %{buildroot}/etc/httpd/httpd.conf

%post
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    # this is initial installation
    if ! getent group apache >/dev/null; then
        groupadd -g 25 apache
    fi
    if ! getent passwd apache >/dev/null; then
        useradd -c "Apache Server" -d /srv/www -g apache \
            -s /bin/false -u 25 apache
    fi

    if [ -h /etc/mime.types ]; then
        mv /etc/mime.types /etc/mime.types.orig
    fi
fi

ln -sf /etc/httpd/conf/mime.types /etc/mime.types
mkdir -p /var/run/httpd
%systemd_post httpd.service

%preun
%systemd_preun httpd.service

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
%systemd_postun_with_restart httpd.service

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files docs
%defattr(-,root,root)
%{_sysconfdir}/httpd/manual/*

%files
%defattr(-,root,root)
%{_libdir}/httpd/*
%{_libdir}/systemd/system/httpd.service
%{_bindir}/*
%exclude %{_bindir}/apxs
%exclude %{_bindir}/dbmmanage
%{_sbindir}/*
%{_datadir}/*
%{_sysconfdir}/httpd/build/*
%{_sysconfdir}/httpd/cgi-bin/*
%{_sysconfdir}/httpd/conf/extra
%{_sysconfdir}/httpd/conf/original
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%{_sysconfdir}/httpd/conf/envvars
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%{_sysconfdir}/httpd/conf/mime.types
%{_sysconfdir}/httpd/error/*
%{_sysconfdir}/httpd/htdocs/*
%{_sysconfdir}/httpd/icons/*
%{_sysconfdir}/httpd/httpd.conf
%dir %{_sysconfdir}/httpd/logs

%files tools
%defattr(-,root,root)
%{_bindir}/apxs
%{_bindir}/dbmmanage

%changelog
*   Thu Apr 25 2019 Dweep Advani <dadvani@vmware.com> 2.4.39-1
-   Upgrading to 2.4.39 for fixing multiple CVEs
-   (1) CVE-2018-17189 (2) CVE-2018-17199 (3) CVE-2019-0190
-   (4) CVE-2019-0211 (5) CVE-2019-0215 (6) CVE-2019-0217
*   Wed Jan 09 2019 Anish Swaminathan <anishs@vmware.com> 2.4.37-1
-   Updated to version 2.4.37, fix CVE-2018-11763
*   Wed Aug 29 2018 Tapas Kundu <tkundu@vmware.com> 2.4.34-1
-   Updated to version 2.4.34, fix CVE-2018-1333
*   Thu Apr 19 2018 Xiaolin Li <xiaolinl@vmware.com> 2.4.33-1
-   Updated to version 2.4.33, fix CVE-2018-1303
*   Wed Oct 04 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.28-1
-   Updated to version 2.4.28
*   Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 2.4.27-3
-   Release bump for expat version update
*   Tue Aug 08 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-2
-   Add shadow to requires
*   Mon Jul 24 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-1
-   Updated to version 2.4.27
*   Fri Jun 23 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.25-3
-   Removed packaging of debug files
*   Thu Apr 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-2
-   Fixing httpd.pid file write issue
*   Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-1
-   Updated to version 2.4.25
*   Wed Dec 21 2016 Anish Swaminathan <anishs@vmware.com>  2.4.18-6
-   Change config file properties for httpd.conf
*   Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 2.4.18-5
-   Added patch for CVE-2016-5387
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.18-4
-   GA - Bump release of all rpms
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.4.18-3
-   Adding upgrade support in pre/post/un script.
*   Mon Mar 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.18-2
-   Fixing systemd service
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.18-1
-   Updated to version 2.4.18
*   Mon Nov 23 2015 Sharath George <sharathg@vmware.com> 2.4.12-4
-   Add /etc/mime.types
*   Tue Sep 29 2015 Xiaolin Li <xiaolinl@vmware.com> 2.4.12-3
-   Move perl script to tools package.
*   Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-2
-   Added service file. Changed installation paths.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-1
-   Initial build. First version
