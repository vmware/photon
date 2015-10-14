Summary:	Utilities for loading kernel modules
Name:		kmod
Version:	16
Release:	2%{?dist}
License:	GPLv2+
URL:		http://www.kernel.org/pub/linux/utils/kernel/kmod
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
%define sha1 kmod=1b3e8066208098b3b9593b63bff5838a41bbdfb0
BuildRequires:	xz-devel
Requires:	xz
%description
The Kmod package contains libraries and utilities for loading kernel modules

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, header files and documentation for developing applications that use %{name}

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--sysconfdir=%{_sysconfdir} \
	--with-rootlibdir=%{_lib} \
	--disable-manpages \
	--with-xz \
	--with-zlib \
	--disable-silent-rules
make VERBOSE=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} pkgconfigdir=%{_libdir}/pkgconfig install
install -vdm 755 %{buildroot}/sbin
for target in depmod insmod modinfo modprobe rmmod; do
	ln -sv /bin/kmod %{buildroot}/sbin/$target
done
ln -sv kmod %{buildroot}/bin/lsmod
find %{buildroot} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
/bin/*
%{_lib}/*.so.*
/sbin/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/bash-completion/completions/kmod

%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 16-2
-   Move development libraries and header files to devel package.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 16-1
-	Initial build. First version	
