Summary:        The Apache HTTP Server
Name:           httpd
Version:        2.4.34
Release:        3%{?dist}
License:        Apache License 2.0
URL:            http://httpd.apache.org/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://apache.mirrors.hoobly.com//httpd/%{name}-%{version}.tar.bz2
%define sha1    httpd=94d6e274273903ed153479c7701fa03761abf93d
Patch0:         http://www.linuxfromscratch.org/patches/blfs/svn/httpd-2.4.27-blfs_layout-1.patch
Patch1:         httpd-uncomment-ServerName.patch
Patch2:         httpd-CVE-2018-11763.patch
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  apr
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  openldap
BuildRequires:  expat-devel
BuildRequires:  lua-devel
Requires:       pcre
Requires:       apr-util
Requires:       openssl
Requires:       openldap
Requires:       lua
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
Provides:       apache2

%define _confdir %{_sysconfdir}

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
%patch2 -p1

%build
%configure \
            --sysconfdir=%{_confdir}/httpd/conf    \
            --libexecdir=%{_libdir}/httpd/modules  \
            --datadir=%{_sysconfdir}/httpd         \
            --enable-authnz-fcgi                   \
            --enable-mods-shared="all cgi"         \
            --enable-mpms-shared=all               \
            --with-apr=%{_prefix}                  \
            --with-apr-util=%{_prefix}             \
            --enable-layout=RPM
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}/usr/lib/systemd/system

cat << EOF >> %{buildroot}/usr/lib/systemd/system/httpd.service
[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/var/run/httpd.pid
ExecStart=/usr/sbin/httpd -k start
ExecStop=/usr/sbin/httpd -k stop
ExecReload=/usr/sbin/httpd -k graceful

[Install]
WantedBy=multi-user.target

EOF

install -vdm755 %{buildroot}/usr/lib/systemd/system-preset
echo "disable httpd.service" > %{buildroot}/usr/lib/systemd/system-preset/50-httpd.preset

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
%{_bindir}/*
%exclude %{_bindir}/apxs
%exclude %{_bindir}/dbmmanage
%{_sbindir}/*
%{_datadir}/*
%{_sysconfdir}/httpd/html/index.html
%{_sysconfdir}/httpd/conf/extra
%{_sysconfdir}/httpd/conf/original
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%{_sysconfdir}/httpd/conf/envvars
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%{_sysconfdir}/httpd/conf/mime.types
%{_sysconfdir}/httpd/error/*
%{_sysconfdir}/httpd/icons/*
%{_sysconfdir}/httpd/httpd.conf
%{_libdir}/systemd/system/httpd.service
%{_libdir}/systemd/system-preset/50-httpd.preset
%{_localstatedir}/log/httpd

%files tools
%defattr(-,root,root)
%{_bindir}/apxs
%{_bindir}/dbmmanage

%changelog
*   Thu Mar 7 2019 Michelle Wang <michellew@vmware.com> 2.4.34-3
-   Update build configure for httpd
*   Thu Jan 24 2019 Dweep Advani <dadvani@vmware.com> 2.4.34-2
-   Fixed CVE-2018-11763
*   Wed Aug 29 2018 Tapas Kundu <tkundu@vmware.com> 2.4.34-1
-   Updated to version 2.4.34, fix CVE-2018-1333
*   Mon Oct 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.28-1
-   Updated to version 2.4.28
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.27-3
-   Remove shadow from requires and use explicit tools for post actions
*   Mon Aug 07 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-2
-   Add shadow to requires for useradd/groupadd
*   Mon Jul 24 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-1
-   Updated to version 2.4.27 - Fixes CVE-2017-3167
*   Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.4.25-3
-   Provide preset file to disable service by default.
*   Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-2
-   Fixing httpd.pid file write issue
*   Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-1
-   Updated to version 2.4.25
*   Tue Dec 27 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.18-8
-   BuildRequires lua, Requires lua.
*   Wed Dec 21 2016 Anish Swaminathan <anishs@vmware.com>  2.4.18-7
-   Change config file properties for httpd.conf
*   Thu Jul 28 2016 Divya Thaluru <dthaluru@vmware.com> 2.4.18-6
-   Removed packaging of debug files
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
