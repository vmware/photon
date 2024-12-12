Summary:         Programs for finding and viewing man pages
Name:            man-db
Version:         2.11.1
Release:         3%{?dist}
URL:             http://www.nongnu.org/man-db
Group:           Applications/System
Vendor:          VMware, Inc.
Distribution:    Photon
Source0:         http://download.savannah.nongnu.org/releases/man-db/%{name}-%{version}.tar.xz
%define sha512   man-db=249d65d01d83feac2503bfc1fba6d018ea0f7485c1112f1bfb4849ef7fbc3c1a50b97ab0844a7792d83bb1084a89abb4fa309ce1bc2bdf1183fe35b9e4f06263
Source1:         %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

Requires:        libpipeline
Requires:        gdbm
Requires:        xz
Requires:        groff
Requires(pre):   systemd-rpm-macros
Requires(pre):   /usr/sbin/useradd /usr/sbin/groupadd

%if 0%{?with_check}
BuildRequires:   shadow
%endif
BuildRequires:   libpipeline-devel
BuildRequires:   gdbm-devel
BuildRequires:   xz
BuildRequires:   groff
BuildRequires:   systemd
BuildRequires:   systemd-devel
Requires:        systemd

%description
The Man-DB package contains programs for finding and viewing man pages.

%prep
%autosetup -n %{name}-%{version}
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
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot}%{_libdir} -name '*.la' -delete
%find_lang %{name} --all-name
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%if 0%{?with_check}
%check
%sysusers_create_compat %{SOURCE1}
make %{?_smp_mflags} check
%endif

%pre
%sysusers_create_compat %{SOURCE1}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

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
%{_sysusersdir}/%{name}.sysusers

%changelog
*   Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 2.11.1-3
-   Release bump for SRP compliance
*   Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 2.11.1-2
-   Use systemd-rpm-macros for user creation
*   Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 2.11.1-1
-   Automatic Version Bump
*   Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 2.11.0-1
-   Automatic Version Bump
*   Tue Jun 07 2022 Gerrit Photon <photon-checkins@vmware.com> 2.10.2-1
-   Automatic Version Bump
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9.3-1
-   Automatic Version Bump
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
