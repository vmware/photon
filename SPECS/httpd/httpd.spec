Summary:    The Apache HTTP Server
Name:       httpd
Version:    2.4.12
Release:    2%{?dist}
License:    Apache License 2.0
URL:        http://httpd.apache.org/
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon
Source0:        http://archive.apache.org/dist/httpd/%{name}-%{version}.tar.bz2
%define sha1 httpd=bc4681bfd63accec8d82d3cc440fbc8264ce0f17
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: apr
BuildRequires: apr-util
BuildRequires: expat
Requires:   pcre
Requires:   apr-util
Requires:   openssl
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

%prep
%setup -q
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
Type=notify

ExecStart=/usr/sbin/httpd \$OPTIONS -DFOREGROUND
ExecReload=/usr/sbin/httpd \$OPTIONS -k graceful
KillSignal=SIGWINCH
KillMode=mixed
Restart=always

[Install]
WantedBy=multi-user.target

EOF

%post
/sbin/ldconfig
if ! getent group apache >/dev/null; then
    groupadd -g 25 apache
fi
if ! getent passwd apache >/dev/null; then
    useradd -c "Apache Server" -d /srv/www -g apache \
        -s /bin/false -u 25 apache
fi

%postun
/sbin/ldconfig
if getent passwd apache >/dev/null; then
    userdel apache
fi
if getent group apache >/dev/null; then
    groupdel apache
fi

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files docs
%defattr(-,root,root)
%{_sysconfdir}/httpd/manual/*

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/*
%{_sysconfdir}/httpd/build/*
%{_sysconfdir}/httpd/cgi-bin/*
%{_sysconfdir}/httpd/conf/*
%{_sysconfdir}/httpd/error/*
%{_sysconfdir}/httpd/htdocs/*
%{_sysconfdir}/httpd/icons/*
%dir %{_sysconfdir}/httpd/logs


%changelog
*   Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-2
-   Added service file. Changed installation paths.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-1
-   Initial build. First version
