Summary: 	Utilities for writing cds.
Name: 		cdrkit
Version: 	1.1.11
Release: 	4%{?dist}
License: 	GPLv2+
Group: 		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0: 	%{name}-%{version}.tar.gz
%define sha1 cdrkit=3f7ddc06db0272942e1a4cd98c3c96462df77387
URL:  		http://gd.tuwien.ac.at/utils/schilling/cdrtools/
Patch0:		cdrkit-1.1.9-efi-boot.patch
BuildArch: x86_64
Requires: 	bash
Requires: 	libcap
BuildRequires: 	cmake
BuildRequires: 	libcap-devel
BuildRequires: 	bzip2-devel
%description
The Cdrtools package contains CD recording utilities. These are useful for reading, creating or writing (burning) Compact Discs.
%prep
%setup -q
%patch0 -p1

%build
make %{?_smp_mflags}

%install
env PREFIX=%{buildroot}%{_prefix} make install
ln -s  genisoimage  %{buildroot}%{_prefix}/bin/mkisofs

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/man/*
%changelog
*   Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 1.1.11-4
-   Replaced BuildArchitectures as BuildArch
*   Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.11-3
-   Support for efi boot (.patch)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.11-2
-   GA - Bump release of all rpms
*   Sat Feb 14 2015 Sharath George <sharathg@vmware.com>
-   first packaging

