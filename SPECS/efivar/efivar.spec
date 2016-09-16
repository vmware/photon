Summary:	Tools and libraries to manipulate EFI variables
Name:		efivar
Version:	0.20
Release:	3%{?dist}
License:	GPLv2
URL:		https://github.com/rhinstaller/efivar/
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/rhinstaller/efivar/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha1 efivar=a66a6d00b59bffe07cbdfc98c727d749157d4140
Patch0:     workaround-rename-of-linux-nvme.h.patch
BuildRequires: popt-devel
%description
efivar provides a simle CLI to the UEFI variable facility
%prep
%setup -q
%patch0 -p1
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
%{_lib64dir}/*
%{_includedir}/*
%{_datadir}/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.20-3
-	GA - Bump release of all rpms
*	Thu Apr 28 2016 Xiaolin Li <xiaolinl@vmware.com> 0.20-2
-	Fix build for linux 4.4.
*	Mon Jul 6 2015 Sharath George <sharathg@vmware.com> 0.20-1
-	Initial build.	First version
