Summary:	Tools and libraries to manipulate EFI variables
Name:		efivar
Version:	0.20
Release:	1%{?dist}
License:	GPLv2
URL:		https://github.com/rhinstaller/efivar/
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://github.com/rhinstaller/efivar/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha1 efivar=a66a6d00b59bffe07cbdfc98c727d749157d4140
BuildRequires: popt-devel
%description
efivar provides a simle CLI to the UEFI variable facility
%prep
%setup -q
%build
make %{?_smp_mflags} PREFIX=%{_prefix} \
    libdir=%{_libdir} \
    bindir=%{_bindir}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    install 

%clean
rm -rf %{buildroot}/*
%files 
%defattr(-,root,root)
%{_bindir}/*
%{_lib64dir}/*
%{_includedir}/*
%{_datadir}/*
%changelog
*	Mon Jul 6 2015 Sharath George <sharathg@vmware.com> 0.20-1
-	Initial build.	First version
