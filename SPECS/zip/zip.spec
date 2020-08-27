Summary:	zip-3.0
Name:		zip
Version:	3.0
Release:	3%{?dist}
License:	BSD
URL:		http://downloads.sourceforge.net/infozip
Source0:	http://downloads.sourceforge.net/infozip/zip30.tar.gz
%define sha1 zip=c9f4099ecf2772b53c2dd4a8e508064ce015d182
Patch0:		zip-passwd-as-stdin.patch
Group:		SystemUtilities
Vendor:		VMware, Inc.
Distribution: Photon
%description
The Zip package contains Zip utilities.
%prep
%setup -qn zip30
%patch0 -p1
%build
make -f unix/Makefile generic_gcc %{?_smp_mflags}
%install
install -v -m755 -d %{buildroot}%{_bindir}
make prefix=%{buildroot}/%{_prefix} MANDIR=%{buildroot}/usr/share/man/man1 -f unix/Makefile install
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*
%changelog
*       Fri Aug 28 2020 Prashant Singh Chauhan <psinghchauha@vmware.com> 3.0-3
*       Added one compiler flags to give passwd as stdin
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-2
-	GA - Bump release of all rpms
*	Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
-	Initial build. First version
