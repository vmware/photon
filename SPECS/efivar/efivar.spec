Summary:	Tools and libraries to manipulate EFI variables
Name:		efivar
Version:	37
Release:	1%{?dist}
License:	GPLv2
URL:		https://github.com/rhboot/efivar
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/rhboot/efivar/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha1 efivar=1ef24e0a06e1a42d7a93ba7a76b2970659c7c0c0
Patch0:         util-h-add-unlikely-and-likely-macros.patch
Patch1:         dp-h-make-format_guid-handle-misaligned-guid-pointers-safely.patch
Patch2:         Fix-all-the-places-Werror-address-of-packed-member-catches.patch
BuildRequires: popt-devel
%description
efivar provides a simle CLI to the UEFI variable facility

%package    devel
Summary:    Header and development files for efivar
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make %{?_smp_mflags} PREFIX=%{_prefix} \
    libdir=%{_libdir} \
    bindir=%{_bindir}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    install

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_lib64dir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_lib64dir}/*.so
%{_lib64dir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 37-1
-   Automatic Version Bump
*   Thu Apr 02 2020 Alexey Makhalov <amakhalov@vmware.com> 36-2
-   Fix compilation issue with gcc-8.4.0
*   Tue Sep 18 2018 Sujay G <gsujay@vmware.com> 36-1
-   Bump efivar version to 36
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 31-1
-   Version update. Added -devel subpackage.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.20-3
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Xiaolin Li <xiaolinl@vmware.com> 0.20-2
-   Fix build for linux 4.4.
*   Mon Jul 6 2015 Sharath George <sharathg@vmware.com> 0.20-1
-   Initial build.	First version
