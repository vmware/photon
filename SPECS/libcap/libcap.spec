Summary:	Libcap
Name:		libcap
Version:	2.25
Release:	4%{?dist}
License:	GPLv2+
URL:		https://www.gnu.org/software/hurd/community/gsoc/project_ideas/libcap.html
Source0:	https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz
%define sha1 libcap=f0b102e4a68e1bbdcb6b143b63c34a250e473088
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	attr
BuildRequires:	attr-devel
%description
The libcap package implements the user-space interfaces to the POSIX 1003.1e capabilities available 
in Linux kernels. These capabilities are a partitioning of the all powerful root privilege 
into a set of distinct privileges.

%package        devel
Summary:        Development files for libcap
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libcap-devel package contains libraries, header files and documentation
for developing applications that use libcap.

%prep
%setup -q
%build
sed -i 's:LIBDIR:PAM_&:g' pam_cap/Makefile
make %{?_smp_mflags}
%install
make prefix=%{_prefix}	SBINDIR=%{_sbindir} PAM_LIBDIR=%{_libdir} RAISE_SETFCAP=no DESTDIR=%{buildroot} install
chmod -v 755 %{buildroot}/usr/lib64/libcap.so
%check
cd progs
./quicktest.sh
%files
%defattr(-,root,root)
%{_lib64dir}/libcap.so.*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_lib64dir}/libcap.a
%{_lib64dir}/pkgconfig/*
%{_lib64dir}/libcap.so

%changelog
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.25-4
-   BuildRequired attr-devel.
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.25-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25-2
-   GA - Bump release of all rpms
*   Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 2.25-1
-   Updating Version.
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.24-2
-   Moving static lib files to devel package.
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.24-1
-   Initial version
