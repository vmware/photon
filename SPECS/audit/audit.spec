Summary:	Kernel Audit Tool
Name:		audit
Version:	2.4.4
Release:	1%{?dist}
Source0:	http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
%define sha1 audit=ad38f3352e21716e86d73b4e06cc41a5e85882ee
License:	GPLv2+
Group:		System Environment/Security
URL:		http://people.redhat.com/sgrubb/audit/
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildRequires:	krb5
BuildRequires:	openldap
BuildRequires:	go
BuildRequires:	tcp_wrappers-devel
BuildRequires:	libcap-ng-devel
BuildRequires:	swig
Requires:	krb5
Requires:	openldap
Requires:	python2
Requires:	tcp_wrappers
Requires:	libcap-ng

%description
The audit package contains the user space utilities for
storing and searching the audit records generate by
the audit subsystem in the Linux 2.6 kernel.

%package devel
Summary:	The libraries and header files needed for audit development.
Requires: 	%{name} = %{version}-%{release}

%description devel
The libraries and header files needed for audit development.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--exec_prefix=/usr \
	--sbindir=%{_sbindir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--with-python=yes \
	--without-python3 \
        --with-libwrap \
	--enable-gssapi-krb5=yes \
        --with-libcap-ng=yes \
	--with-aarch64 \
        --enable-zos-remote \
	--with-golang \
	--enable-systemd

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%post
/sbin/ldconfig
%systemd_post auditd.service

%preun
%systemd_preun auditd.service

%postun
/sbin/ldconfig

%files 
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/python*/*
%{_libdir}/golang/*
%{_libdir}/systemd/system/auditd.service
%{_libexecdir}/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_sysconfdir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h

%changelog
* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.4.4-1
- Initial version
