Name:	metapackage
Summary:	This package contains the container bootstrap files. 
Version:	0.1
Release:	1%{?dist}
License:	GPLv2
Requires:	gcc, binutils, make, glibc-devel, linux-api-headers

%description
This package is to meant install the necessary packages to a minimal photon iso

%prep

%build

%files
%defattr(-,root,root,0755)
