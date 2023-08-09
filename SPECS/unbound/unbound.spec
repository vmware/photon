Summary:        unbound dns server
Name:           unbound
Version:        1.17.0
Release:        3%{?dist}
Group:          System/Servers
Vendor:         VMware, Inc.
License:        BSD
Distribution:   Photon
URL:            http://www.unbound.net
Source0:        https://www.unbound.net/downloads/%{name}-%{version}.tar.gz
%define sha512  unbound=f6b9f279330fb19b5feca09524959940aad8c4e064528aa82b369c726d77e9e8e5ca23f366f6e9edcf2c061b96f482ed7a2c26ac70fc15ae5762b3d7e36a5284
Source1:        %{name}.service
Source2:        %{name}.sysusers
Requires:       systemd
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  expat-devel
Requires(pre):  systemd-rpm-macros
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package        devel
Summary:        unbound development libs and headers
Group:          Development/Libraries
Requires:       expat-devel

%description    devel
Development files for unbound dns server

%package        docs
Summary:        unbound docs
Group:          Documentation

%description    docs
unbound dns server docs

%prep
%autosetup

%build
%configure \
    --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \
    --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
install -vdm755 %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%check
make check %{?_smp_mflags}

%pre
%sysusers_create_compat %{SOURCE2}

%post
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_sbindir}/*
%{_sysconfdir}/*
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.sysusers

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files docs
%{_mandir}/*

%changelog
*  Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.17.0-3
-  Resolving systemd-rpm-macros for group creation
*  Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.17.0-2
-  Use systemd-rpm-macros for user creation
*  Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 1.17.0-1
-  Automatic Version Bump
*  Tue Sep 27 2022 Gerrit Photon <photon-checkins@vmware.com> 1.16.3-1
-  Automatic Version Bump
*  Wed Aug 24 2022 Srish Srinivasan <ssrish@vmware.com> 1.16.2-1
-  Updated to version 1.16.2
*  Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.16.1-1
-  Automatic Version Bump
*  Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.15.0-1
-  Automatic Version Bump
*  Fri Jul 30 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.0-2
-  Fix openssl 3.0.0 compatibility with unbound
*  Thu Mar 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.0-1
-  Update to 1.12.0 for openssl 3.0 compatibility
*  Tue Feb 02 2021 Shreyas B. <shryasb@vmware.com> 1.11.0-2
-  Fix for CVE-2020-28935
*  Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1.11.0-1
-  Automatic Version Bump
*  Sun May 24 2020 Shreyas B. <shryasb@vmware.com> 1.8.0-4
-  Fix for CVE-2020-12662 & CVE-2020-12663
*  Fri Dec 20 2019 Shreyas B. <shryasb@vmware.com> 1.8.0-3
-  Fix for vulnerability CVE-2019-18934 that can cause shell code
-  execution after receiving a specially crafted answer.
*  Mon Oct 14 2019 Shreyas B. <shryasb@vmware.com> 1.8.0-2
-  Fix for CVE-2019-16866.
*  Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 1.8.0-1
-  Update to version 1.8.0.
*  Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-3
-  Remove shadow from requires and use explicit tools for post actions
*  Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-2
-  Requires expat-devel
*  Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.6.1-1
-  Updated to version 1.6.1
*  Fri Jan 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-1
-  Initial.
