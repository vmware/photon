%define with_golang 0

Summary:        Kernel Audit Tool
Name:           audit
Version:        2.8.5
Release:        25%{?dist}
Patch0:         audit-2.8.5-gcc-10.patch
License:        GPLv2+
Group:          System Environment/Security
URL:            http://people.redhat.com/sgrubb/audit/
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
%define sha512 audit=7d416aaa21c1a167f8e911ca82aecbaba804424f3243f505066c43ecc4a62a34feb2c27555e99d3268608404793dccca0f828c63670e3aa816016fb493f8174a

BuildRequires:  krb5-devel
BuildRequires:  openldap
BuildRequires:  tcp_wrappers-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  swig
BuildRequires:  e2fsprogs-devel
BuildRequires:  systemd
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if 0%{?with_golang}
BuildRequires:  go
%endif

Requires:       systemd
Requires:       krb5
Requires:       openldap
Requires:       tcp_wrappers
Requires:       libcap-ng
Requires:       gawk

%description
The audit package contains the user space utilities for
storing and searching the audit records generate by
the audit subsystem in the Linux 2.6 kernel.

%package        devel
Summary:        The libraries and header files needed for audit development.
Requires:       %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for audit development.

%package  -n    python3-audit
Summary:        Python3 bindings for libaudit
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-audit
The python3-audit package contains the python2 bindings for libaudit
and libauparse.

%prep
%autosetup -p1

%build
%configure \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    --exec_prefix=/usr \
    --with-python3=yes \
    --with-libwrap \
    --enable-gssapi-krb5=yes \
    --with-libcap-ng=yes \
    --with-aarch64 \
    --enable-zos-remote \
%if 0%{?with_golang}
    --with-golang \
%endif
    --enable-systemd \
    --disable-static

make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/{etc/audispd/plugins.d,etc/audit/rules.d}
mkdir -p %{buildroot}%{_var}/log/audit
mkdir -p %{buildroot}%{_var}/spool/audit
%make_install

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable auditd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-auditd.preset

%check
make %{?_smp_mflags} check

%pretrans -p <lua>
path = "/var/log/audit"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%post
/sbin/ldconfig
%systemd_post  auditd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart auditd.service

%preun
%systemd_preun auditd.service

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%{_libdir}/systemd/system/auditd.service
%{_libdir}/systemd/system-preset/50-auditd.preset
%{_libexecdir}/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%dir %{_var}/log/audit
%{_var}/spool/audit
%attr(750,root,root) %dir %{_sysconfdir}/audit
%attr(750,root,root) %dir %{_sysconfdir}/audit/rules.d
%attr(750,root,root) %dir %{_sysconfdir}/audisp
%attr(750,root,root) %dir %{_sysconfdir}/audisp/plugins.d
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/auditd.conf
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/rules.d/audit.rules
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audit.rules
%ghost %config(noreplace) %attr(640,root,root) %{_sysconfdir}/audit/audit-stop.rules
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/audispd.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/plugins.d/af_unix.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/plugins.d/syslog.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/plugins.d/audispd-zos-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/zos-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/audisp-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/audisp/plugins.d/au-remote.conf
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/libaudit.conf

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%if 0%{?with_golang}
%{_libdir}/golang/*
%endif
%{_includedir}/*.h
%{_mandir}/man3/*
/usr/share/aclocal/audit.m4

%files -n python3-audit
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 2.8.5-25
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-24
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-23
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-22
- Bump up version to compile with new go
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.8.5-21
- Remove .la files
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-20
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-19
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-18
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-17
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-16
- Bump up version to compile with new go
* Thu Feb 10 2022 Piyush Gupta <gpiyush@vmware.com> 2.8.5-15
- Bump up version to compile with new go.
* Wed Feb 09 2022 Dweep Advani <dadvani@vmware.com> 2.8.5-14
- Fixed pretrans unknown script error during ova build
* Thu Jan 20 2022 Dweep Advani <dadvani@vmware.com> 2.8.5-13
- Fixed package upgrade issue
* Wed Jan 05 2022 Dweep Advani <dadvani@vmware.com> 2.8.5-12
- Use /var/log/audit
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.8.5-11
- Bump up to compile with python 3.10
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 2.8.5-10
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 2.8.5-9
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.8.5-8
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 2.8.5-7
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.8.5-6
- Bump up version to compile with new go
* Thu Jan 21 2021 Alexey Makhalov <amakhalov@vmware.com> 2.8.5-5
- GCC-10 support
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.8.5-4
- Bump up version to compile with new go
* Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 2.8.5-3
- Mass removal python2
* Tue Nov 26 2019 Alexey Makhalov <amakhalov@vmware.com> 2.8.5-2
- Cross compilation support.
- Do not use BuildRequires in subpackages.
- Disable golang dependency.
* Thu Oct 17 2019 Shreyas B <shreyasb@vmware.com> 2.8.5-1
- Updated to version 2.8.5.
* Mon Sep 3 2018 Keerthana K <keerthanak@vmware.com> 2.8.4-1
- Updated to version 2.8.4.
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  2.7.5-4
- Fixed the log file directory structure
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.7.5-3
- Disabled audit service by default
* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.5-2
- Move python2 requires to python subpackage and added python3.
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.7.5-1
- Version update.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-7
- Moved man3 to devel subpackage.
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.5-6
- Required krb5-devel.
* Fri Jul 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5-5
- Add gawk requirement.
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-4
- Fixed logic to restart the active services after upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5-3
- GA - Bump release of all rpms
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  2.5-2
- Fixing spec file to handle rpm upgrade scenario correctly
* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  2.5-1
- Upgrade to 2.5
* Fri Jan 29 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-4
- Add directories for auditd service.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  2.4.4-3
- Change config file attributes.
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 2.4.4-2
- Add systemd requirement.
* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.4.4-1
- Initial version
