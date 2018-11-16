Summary:        Linux Pluggable Authentication Modules
Name:           Linux-PAM
Version:        1.3.0
Release:        2%{?dist}
License:        BSD and GPLv2+
URL:            https://www.kernel.org/pub/linux/libs/pam/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://linux-pam.org/library/%{name}-%{version}.tar.bz2
%define sha1    Linux-PAM=e956252e81d824c35a60c9b50919ca0767f8a8ec
BuildRequires:  cracklib-devel
Requires:       cracklib
%description
The Linux PAM package contains Pluggable Authentication Modules used to
enable the local system administrator to choose how applications authenticate users.

%package lang
Summary: Additional language files for Linux-PAM
Group: System Environment/Base
Requires:       %{name} = %{version}-%{release}
%description lang
These are the additional language files of Linux-PAM.

%package        devel
Summary:        Development files for Linux-PAM
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    devel
The Linux-PAM-devel package contains libraries, header files and documentation
for developing applications that use Linux-PAM.

%prep
%setup -q
%build

%configure \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    --includedir=/usr/include/security \
    --sbindir=/sbin \
    --enable-securedir=/usr/lib/security \
    --docdir=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
chmod -v 4755 %{buildroot}/sbin/unix_chkpwd
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
ln -sf pam_unix.so %{buildroot}/usr/lib/security/pam_unix_auth.so
ln -sf pam_unix.so %{buildroot}/usr/lib/security/pam_unix_acct.so
ln -sf pam_unix.so %{buildroot}/usr/lib/security/pam_unix_passwd.so
ln -sf pam_unix.so %{buildroot}/usr/lib/security/pam_unix_session.so
find %{buildroot}/%{_libdir} -name '*.la' -delete
find %{buildroot}/usr/lib/ -name '*.la' -delete
%{find_lang} Linux-PAM

%{_fixperms} %{buildroot}/*

%check
install -v -m755 -d /etc/pam.d
cat > /etc/pam.d/other << "EOF"
auth     required       pam_deny.so
account  required       pam_deny.so
password required       pam_deny.so
session  required       pam_deny.so
EOF
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_sysconfdir}/*
/sbin/*
%{_lib}/security/*
%{_libdir}/*.so*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files lang -f Linux-PAM.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_docdir}/%{name}-%{version}/*

%changelog
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-2
-   Cross compilation support
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-1
-   Version update.
*   Fri Feb 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-5
-   Added pam_unix_auth.so, pam_unix_acct.so, pam_unix_passwd.so,
-   and pam_unix_session.so.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-4
-   Added devel subpackage.
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> 1.2.1-3
-   Packaging pam cracklib module
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-2
-   GA - Bump release of all rpms
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-1
-   Updated to version 1.2.1
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.1.8-2
-   Update according to UsrMove.
*   Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.8-1
-   Initial build.  First version
