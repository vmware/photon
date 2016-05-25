Summary:	Check-0.10.0
Name:		check
Version:	0.10.0
Release:	2%{?dist}
License:	LGPLv2+
URL:		http://check.sourceforge.net/
Source0:	http://sourceforge.net/projects/check/files/latest/download/%{name}-%{version}.tar.gz
%define sha1 check=35d3a53446aea7b21a770faedb358d0fc7cba76d
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: Photon
%description
Check is a unit testing framework for C. It features a simple interface for defining unit tests, 
putting little in the way of the developer. Tests are run in a separate address space, 
so both assertion failures and code errors that cause segmentation faults or other signals can be caught.
%prep
%setup -q
%build
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
rm %{buildroot}%{_infodir}/dir
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*so*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_mandir}/man1/*
%{_infodir}/*
/usr/share/doc/%{name}/*
/usr/share/aclocal/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	0.10.0-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 0.10.0-1
-   Updated to version 0.10.0
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 0.9.14-2
-   Updated group.
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.9.14-1
-	Initial build. First version
