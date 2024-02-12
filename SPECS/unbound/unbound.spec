Summary:        unbound dns server
Name:           unbound
Version:        1.16.3
Release:        2%{?dist}
Group:          System/Servers
Vendor:         VMware, Inc.
License:        BSD
Distribution:   Photon
URL:            http://www.unbound.net

Source0: https://www.unbound.net/downloads/%{name}-%{version}.tar.gz
%define sha512 unbound=ef5cda926dd1082a750615d8687bccd756869c66e9f24f984fda4c6613f94f3e4884db328b8d7b490777a75d3e616dcb61c5258e7777923c0590e6fabacd207c

Source1:        %{name}.service

Patch0: CVE-2023-50387-CVE-2023-50868.patch

BuildRequires:  systemd
BuildRequires:  expat-devel

Requires:       systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package    devel
Summary:    unbound development libs and headers
Group:      Development/Libraries
Requires:   expat-devel
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for unbound dns server

%package    docs
Summary:    unbound docs
Group:      Documentation

%description docs
unbound dns server docs

%prep
%autosetup -p1

%build
%configure \
    --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm755 %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
%make_build check

%pre
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
        -c "Unbound DNS resolver" unbound

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_sbindir}/*
%{_sysconfdir}/*
%{_unitdir}/%{name}.service

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files docs
%defattr(-,root,root)
%{_mandir}/*

%changelog
* Mon Feb 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.16.3-2
- Fix CVE-2023-50387, CVE-2023-50868
* Fri Sep 30 2022 Srish S. <ssrish@vmware.com> 1.16.3-1
- Update to version 1.16.3 for fixing CVE-2022-3204
* Thu Aug 18 2022 Srish S. <ssrish@vmware.com> 1.13.1-2
- Fix for CVE-2022-30698 and CVE-2022-30699
* Tue May 04 2021 Shreyas B. <shryasb@vmware.com> 1.13.1-1
- Update to version 1.13.1.
* Tue Feb 02 2021 Shreyas B. <shryasb@vmware.com> 1.8.0-5
- Fix for CVE-2020-28935
* Sun May 24 2020 Shreyas B. <shryasb@vmware.com> 1.8.0-4
- Fix for CVE-2020-12662 & CVE-2020-12663
* Fri Dec 20 2019 Shreyas B. <shryasb@vmware.com> 1.8.0-3
- Fix for vulnerability CVE-2019-18934 that can cause shell code execution after receiving a specially crafted answer.
* Mon Oct 14 2019 Shreyas B. <shryasb@vmware.com> 1.8.0-2
- Fix for CVE-2019-16866.
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 1.8.0-1
- Update to version 1.8.0.
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-3
- Remove shadow from requires and use explicit tools for post actions
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-2
- Requires expat-devel
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.6.1-1
- Updated to version 1.6.1
* Fri Jan 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-1
- Initial
