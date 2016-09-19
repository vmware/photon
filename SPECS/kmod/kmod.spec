Summary:	Utilities for loading kernel modules
Name:		kmod
Version:	21
Release:	4%{?dist}
License:	GPLv2+
URL:		http://www.kernel.org/pub/linux/utils/kernel/kmod
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
%define sha1 kmod=b2c1a0a1f2979fd29c7b0825ed19254c332246b4
Patch0:         kmod-21-fix-return-error-code.patch
BuildRequires:	xz-devel
Requires:	xz
%description
The Kmod package contains libraries and utilities for loading kernel modules
%prep
%setup -q
%patch0 -p1
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
for target in depmod insmod lsmod modinfo modprobe rmmod; do
	ln -sv /bin/kmod %{buildroot}/sbin/$target
done
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
/bin/*
%{_lib}/*.so.*
/sbin/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/bash-completion/completions/kmod
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 21-4
-	GA - Bump release of all rpms
*   Wed Apr 21 2016 Anish Swaminathan <anishs@vmware.com> 21-3
-   Add patch for return code fix in error path
*   Fri Mar 25 2016 Alexey Makhalov <amakhalov@vmware.com> 21-2
-   /bin/lsmod -> /sbin/lsmod
*   Wed Jan 13 2016 Xiaolin Li <xiaolinl@vmware.com> 21-1
-   Updated to version 21
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 16-1
-   Initial build. First version
