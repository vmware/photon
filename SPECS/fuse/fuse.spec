Summary:	File System in Userspace (FUSE) utilities
Name:           fuse
Version:        2.9.4
Release:        2%{?dist}
License:        GPL+
Url:		http://fuse.sourceforge.net/
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        http://sourceforge.net/projects/fuse/files/fuse-2.X/%{version}/%{name}-%{version}.tar.gz
%define sha1 fuse=c8b25419f33624dc5240af6a5d26f2c04367ca71
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

%check
make VERBOSE=1 V=1 %{?_smp_mflags} check

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
make install \
	prefix=%{buildroot}%{_prefix}

install -v -m755 -d /usr/share/doc/fuse-2.9.4 &&
install -v -m644    doc/{how-fuse-works,kernel.txt} \
                    /usr/share/doc/fuse-2.9.4

%files 
%defattr(-, root, root)
%doc README NEWS INSTALL AUTHORS COPYING COPYING.LIB
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
*	Fri Aug 28 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.4-2
-	post/pre actions are removed. 
*	Tue Jun 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.4-1
-	Initial version. 

