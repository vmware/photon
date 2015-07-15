Summary:	Linux Pluggable Authentication Modules
Name:		Linux-PAM
Version:	1.1.8
Release:	2%{?dist}
License:	BSD and GPLv2+
URL:		https://www.kernel.org/pub/linux/libs/pam/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://linux-pam.org/library/%{name}-%{version}.tar.bz2
%define sha1 Linux-PAM=f8ce53c67363f78d520392fa1c253c4978058be1
%description
The Linux PAM package contains Pluggable Authentication Modules used to 
enable the local system administrator to choose how applications authenticate users.

%package lang
Summary: Additional language files for Linux-PAM
Group: System Environment/Base
Requires: Linux-PAM >= 1.1.8
%description lang
These are the additional language files of Linux-PAM.

%prep
%setup -q
%build

./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
        --sysconfdir=/etc   \
        --enable-securedir=/usr/lib/security \
        --docdir=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
chmod -v 4755 %{buildroot}/sbin/unix_chkpwd
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
find %{buildroot}/usr/lib/ -name '*.la' -delete
%{find_lang} Linux-PAM

%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_sysconfdir}/*
/sbin/*
%{_lib}/security/*
%{_libdir}/*.so*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_docdir}/%{name}-%{version}/*
%{_includedir}/security/*

%files lang -f Linux-PAM.lang
%defattr(-,root,root)

%changelog
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.1.8-2
-   Update according to UsrMove.
*	Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.8-1
-	Initial build.	First version
