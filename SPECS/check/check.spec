Summary:	Check-0.9.14
Name:		check
Version:	0.9.14
Release:	2%{?dist}
License:	LGPLv2+
URL:		http://check.sourceforge.net/
Source0:	http://sourceforge.net/projects/check/files/latest/download/%{name}-%{version}.tar.gz
%define sha1 check=4b79e2d485d014ddb438e322b64235347d57b0ff
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
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 0.9.14-2
-   Updated group.
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.9.14-1
-	Initial build. First version
