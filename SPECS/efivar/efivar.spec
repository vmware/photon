Summary:       Tools and libraries to manipulate EFI variables
Name:          efivar
Version:       38
Release:       2%{?dist}
URL:           https://github.com/rhboot/efivar
Group:         System Environment/System Utilities
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       https://github.com/rhboot/efivar/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=c2f17297c863ece134a9dd758d237fd2df8c8d072f87af1d0bf2bcf9acfc7a53c25597f03fd4fb8cc664b205743d4ffa0ef1b068d0f73c58fa573d40993f3155
# Generated using mandoc
# mandoc -mdoc -Tman -Ios=Linux efisecdb.1.mdoc > efisecdb.1
Source1:       efisecdb.1

Source2: license.txt
%include %{SOURCE2}

BuildRequires: popt-devel

%description
efivar provides a simle CLI to the UEFI variable facility

%package    devel
Summary:    Header and development files for efivar
Requires:   %{name} = %{version}-%{release}
%description devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1
cp %{SOURCE1} docs
touch docs/efisecdb.1

%build
# This package implements symbol versioning with toplevel ASM statments which is
# incompatible with LTO.  Disable LTO by overiding OPTIMIZE=

%make_build OPTIMIZE="-O2 -Wno-error=stringop-truncation"

%install
%make_install %{?_smp_mflags} LIBDIR=%{_libdir} BINDIR=%{_bindir}

%if 0%{?with_check}
%check
make %{?_smp_mflags} test
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 38-2
- Release bump for SRP compliance
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 38-1
- Automatic Version Bump
- Use pre generated man page for efisecdb.
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 37-2
- GCC-10 support.
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 37-1
- Automatic Version Bump
* Thu Apr 02 2020 Alexey Makhalov <amakhalov@vmware.com> 36-2
- Fix compilation issue with gcc-8.4.0
* Tue Sep 18 2018 Sujay G <gsujay@vmware.com> 36-1
- Bump efivar version to 36
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 31-1
- Version update. Added -devel subpackage.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.20-3
- GA - Bump release of all rpms
* Thu Apr 28 2016 Xiaolin Li <xiaolinl@vmware.com> 0.20-2
- Fix build for linux 4.4.
* Mon Jul 6 2015 Sharath George <sharathg@vmware.com> 0.20-1
- Initial build.    First version
