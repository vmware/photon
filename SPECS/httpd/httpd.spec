Summary:    The Apache HTTP Server
Name:       httpd
Version:    2.4.18
Release:    6%{?dist}
License:    Apache License 2.0
URL:        http://httpd.apache.org/
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon
Source0:        http://archive.apache.org/dist/httpd/%{name}-%{version}.tar.bz2
%define sha1 httpd=271a129f2f04e3aa694e5c2091df9b707bf8ef80
Patch0: http://www.linuxfromscratch.org/patches/blfs/svn/httpd-2.4.18-blfs_layout-1.patch
Patch1: httpd-2.4.18-CVE-2016-5387.patch 
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: apr
BuildRequires: apr-util
BuildRequires: apr-util-devel
BuildRequires: openldap
BuildRequires: expat
Requires:   pcre
Requires:   apr-util
Requires:   openssl
Requires:   openldap
Provides:	apache2
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
PIDFile=/var/run/httpd.pid
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
%{_sysconfdir}/httpd/build/*
%{_sysconfdir}/httpd/cgi-bin/*
%{_sysconfdir}/httpd/conf/*
%{_sysconfdir}/httpd/error/*
%{_sysconfdir}/httpd/htdocs/*
%{_sysconfdir}/httpd/icons/*
%{_sysconfdir}/httpd/httpd.conf
%dir %{_sysconfdir}/httpd/logs
%{_libdir}/systemd/system/httpd.service

%files tools
%defattr(-,root,root)
%{_bindir}/apxs
%{_bindir}/dbmmanage

%changelog
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
