Summary:      zip-3.0
Name:         zip
Version:      3.0
Release:      5%{?dist}
URL:          http://downloads.sourceforge.net/infozip
Group:        SystemUtilities
Vendor:       VMware, Inc.
Distribution: Photon

Source0: http://downloads.sourceforge.net/infozip/zip30.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:       zip-passwd-as-stdin.patch

%description
The Zip package contains Zip utilities.

%prep
%autosetup -p1 -n zip30

%build
make -f unix/Makefile generic_gcc %{?_smp_mflags}

%install
install -v -m755 -d %{buildroot}%{_bindir}
make %{?_smp_mflags} prefix=%{buildroot}/%{_prefix} MANDIR=%{buildroot}/usr/share/man/man1 -f unix/Makefile install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*

%changelog
* Sun Dec 15 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.0-5
- Bump up for generating provenance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.0-4
- Release bump for SRP compliance
* Wed Oct 07 2020 Prashant Singh Chauhan <psinghchauha@vmware.com> 3.0-3
- Added one compiler flags to give passwd as stdin
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-2
- GA - Bump release of all rpms
* Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 3.0-1
- Initial build. First version
