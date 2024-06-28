Summary:        cscope is an interactive C code browser
Name:           cscope
Version:        15.9
Release:        1%{?dist}
License:        BSD
Group:          Development/Tools
URL:            http://cscope.sourceforge.net
Source:         http://downloads.sourceforge.net/cscope/%{name}-%{version}.tar.gz
%define sha1 cscope=e89c6a3458164552d9301ccc213181f463e5210e
Vendor:         VMware, Inc.
Distribution:   Photon

%description
cscope is an interactive, screen-oriented tool that allows the user to browse
through C source files for specified elements of code.

%prep
%setup -q

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
* Tue Feb 25 2020 Siddharth Chandrasekran <csiddharth@vmware.com> 15.9-1
- Initial version for Photon
