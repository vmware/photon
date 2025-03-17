Summary:        cscope is an interactive C code browser
Name:           cscope
Version:        15.9
Release:        2%{?dist}
Group:          Development/Tools
URL:            http://cscope.sourceforge.net
Source0:         http://downloads.sourceforge.net/cscope/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon

%description
cscope is an interactive, screen-oriented tool that allows the user to browse
through C source files for specified elements of code.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
%makeinstall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc TODO COPYING ChangeLog AUTHORS README NEWS INSTALL
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 15.9-2
- Release bump for SRP compliance
* Tue Feb 25 2020 Siddharth Chandrasekran <csiddharth@vmware.com> 15.9-1
- Initial version for Photon
