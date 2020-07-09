Summary:        Programs for finding and viewing man pages
Name:           man-db
Version:        2.9.0
Release:        1%{?dist}
License:        GPLv2+
URL:            http://www.nongnu.org/man-db
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://download.savannah.nongnu.org/releases/man-db/%{name}-%{version}.tar.xz
%define sha1    man-db=807392e422d22d3dc9e9fec3fdd0fe7ce9c53fc7
Requires:       libpipeline
Requires:       gdbm
Requires:       xz
Requires:       groff
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
%if %{with_check}
BuildRequires:  shadow
%endif
BuildRequires:  libpipeline-devel
BuildRequires:  gdbm-devel
BuildRequires:  xz
BuildRequires:  groff
BuildRequires:  systemd
Requires:       systemd

%description
The Man-DB package contains programs for finding and viewing man pages.

%prep
%setup -qn %{name}-%{version}
%build
%configure \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-setuid \
    --with-systemdsystemunitdir=%{_unitdir} \
    --with-browser=%{_bindir}/lynx \
    --with-vgrind=%{_bindir}/vgrind \
    --with-grap=%{_bindir}/grap \
    --disable-silent-rules

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
%find_lang %{name} --all-name

%check
getent group man >/dev/null || groupadd -r man
getent passwd man >/dev/null || useradd -c "man" -d /var/cache/man -g man \
        -s /bin/false -M -r man
make %{?_smp_mflags} check

%pre
getent group man >/dev/null || groupadd -r man
getent passwd man >/dev/null || useradd -c "man" -d /var/cache/man -g man \
        -s /bin/false -M -r man

%post -p /sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
    getent passwd man >/dev/null && userdel man
    getent group man >/dev/null && groupdel man
fi
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_unitdir}/man-db.service
%{_unitdir}/man-db.timer
%config(noreplace) %{_sysconfdir}/man_db.conf
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/man-db/*
%{_libdir}/man-db/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%{_libdir}/tmpfiles.d/man-db.conf

%changelog
*   Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9.0-1
-   Automatic Version Bump
*   Mon Oct 22 2018 Sujay G <gsujay@vmware.com> 2.8.4-1
-   Bump man-db version to 2.8.4
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.7.6-4
-   Remove shadow from requires and use explicit tools for post actions
*   Fri Aug 04 2017 Chang Lee <changlee@vmware.com> 2.7.6-3
-   Setup a testing environment before %check
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.6-2
-   Add gdbm-devel to BuildRequires
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 2.7.6-1
-   Update package version
*   Mon Oct 03 2016 ChangLee <changlee@vmware.com> 2.7.5-5
-   Modified check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.5-4
-   GA - Bump release of all rpms
*   Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> 2.7.5-3
-   Fix user man:man adding.
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.7.5-2
-   Adding support for upgrade in pre/post/un scripts.
*   Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 2.7.5-1
-   Updated to new version.
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.6.6-2
-   Handled locale files with macro find_lang
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.6.6-1
-   Initial build. First version
