Summary:	File System in Userspace (FUSE) utilities
Name:           fuse
Version:        2.9.5
Release:        3%{?dist}
License:        GPL+
Url:		http://fuse.sourceforge.net/
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://github.com/libfuse/libfuse/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha1 fuse=bf71181cdc25f65e5757a8a14d352296722de2e3
Patch0:         fuse-escaped-commas-CVE-2018-10906.patch
Patch1:         fuse-refuse-unknown-options-CVE-2018-10906.patch
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
%patch0 -p1
%patch1 -p1
%build
./configure --prefix=%{_prefix} --disable-static INIT_D_PATH=/tmp/init.d &&
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
make install \
	prefix=%{buildroot}%{_prefix}

install -v -m755 -d /usr/share/doc/fuse-2.9.5 &&
install -v -m644    doc/{how-fuse-works,kernel.txt} \
                    /usr/share/doc/fuse-2.9.5

%files 
%defattr(-, root, root)
%{_libdir}/*
%exclude %{_libdir}/debug/
%exclude %{_libdir}/*.la
%{_bindir}/*
%{_datadir}/man/*

%files devel
%doc ChangeLog 
%{_libdir}/*.la
%{_prefix}/lib/libfuse.so
%{_prefix}/include/*
%{_prefix}/bin/fusermount

%changelog
*	Fri Jan 18 2019 Ankit Jain <ankitja@vmware.com> 2.9.5-3
-	Fix for CVE-2018-10906, added two patches
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.5-2
-	GA - Bump release of all rpms
*   Tue Jan 26 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.5-1
-   Updated to version 2.9.5
*	Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.4-2
-	post/pre actions are removed. 
*	Tue Jun 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.4-1
-	Initial version. 

