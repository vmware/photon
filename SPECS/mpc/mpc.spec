Summary:	Library for the arithmetic of complex numbers
Name:		mpc
Version:	1.0.3
Release:	1%{?dist}
License:	LGPLv3+
URL:		http://www.multiprecision.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://www.multiprecision.org/mpc/download/%{name}-%{version}.tar.gz
Requires:	gmp
%define sha1 mpc=b8be66396c726fdc36ebb0f692ed8a8cca3bcc66
%description
The MPC package contains a library for the arithmetic of complex
numbers with arbitrarily high precision and correct rounding of
the result.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*
%changelog
*       Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  1.0.3-1
-       Update version.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.0.2-1
-	Initial build. First version
