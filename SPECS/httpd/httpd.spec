Summary:    The Apache HTTP Server
Name:       httpd
Version:    2.4.12
Release:    1%{?dist}
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

%prep
%setup -q
%build
./configure --enable-authnz-fcgi                            \
            --enable-mods-shared="all cgi"                  \
            --enable-mpms-shared=all                        \
            --enable-suexec=shared                          \
            --with-apr=%{_prefix}                           \
            --with-apr-util=%{_prefix}                      \
            --with-suexec-bin=/usr/lib/httpd/suexec         \
            --with-suexec-caller=apache                     \
            --with-suexec-docroot=/srv/www                  \
            --with-suexec-logfile=/var/log/httpd/suexec.log \
            --with-suexec-uidmin=100                        \
            --with-suexec-userdir=public_html

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install &&


%post
/sbin/ldconfig
if ! getent group apache >/dev/null; then
    groupadd -g 25 apache
fi
if ! getent passwd apache >/dev/null; then
    useradd -c "Apache Server" -d /srv/www -g apache \
        -s /bin/false -u 25 apache
fi

mv -v /usr/sbin/suexec /usr/lib/httpd/suexec
chgrp apache           /usr/lib/httpd/suexec &&
chmod 4754             /usr/lib/httpd/suexec &&
chown -v -R apache:apache /srv/www

%postun
/sbin/ldconfig
if getent passwd apache >/dev/null; then
    userdel apache
fi
if getent group apache >/dev/null; then
    groupdel apache
fi

%files
%defattr(-,root,root)
/usr/local/*

%changelog
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-1
-   Initial build. First version
