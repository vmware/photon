Summary:	Libcap-2.24
Name:		libcap
Version:	2.24
Release:	1%{?dist}
License:	GPLv2+
URL:		https://www.gnu.org/software/hurd/community/gsoc/project_ideas/libcap.html
Source0:	https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz
%define sha1 libcap=b2754cddb614567de445ffdaac7a00b9671b858a
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	attr
BuildRequires:	attr
%description
The libcap package implements the user-space interfaces to the POSIX 1003.1e capabilities available 
in Linux kernels. These capabilities are a partitioning of the all powerful root privilege 
into a set of distinct privileges.
%prep
%setup -q
%build
sed -i 's:LIBDIR:PAM_&:g' pam_cap/Makefile
make %{?_smp_mflags}
%install
make prefix=%{_prefix}	SBINDIR=%{_sbindir} PAM_LIBDIR=%{_libdir} RAISE_SETFCAP=no DESTDIR=%{buildroot} install
chmod -v 755 %{buildroot}/usr/lib64/libcap.so
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_lib64dir}/*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%changelog
*	Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.24-1
-	Initial version
