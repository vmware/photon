Summary:	File System in Userspace (FUSE) utilities
Name:           fuse
Version:        3.0.1
Release:        1%{?dist}
License:        GPL+
Url:		http://fuse.sourceforge.net/
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://github.com/libfuse/libfuse/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha1 fuse=9362ce52c17c2865ba47f9d4fcb9f054c38bd1fc

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. 

%package	devel
Summary:	Header and development files
Group: 		Development/Libraries
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create fuse applications. 

%prep
%setup -q
%build
./configure --prefix=%{_prefix} --disable-static INIT_D_PATH=/tmp/init.d &&
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
make install \
	prefix=%{buildroot}%{_prefix}

install -v -m755 -d /usr/share/doc/%{name}-%{version} &&
install -v -m644    doc/kernel.txt \
                    /usr/share/doc/%{name}-%{version}

%files 
%defattr(-, root, root)
%{_libdir}/*
%exclude %{_libdir}/debug/
%exclude %{_libdir}/*.la
%{_bindir}/*
%{_datadir}/man/*

%files devel
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_prefix}/lib/libfuse3.so
%{_prefix}/include/*
%{_prefix}/bin/fusermount3
%{_prefix}/sbin/mount.fuse3

%changelog
*	Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 3.0.1-1
-	Upgrade to 3.0.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.5-2
-	GA - Bump release of all rpms
*   Tue Jan 26 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.5-1
-   Updated to version 2.9.5
*	Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.4-2
-	post/pre actions are removed. 
*	Tue Jun 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.4-1
-	Initial version. 

