Summary: A minimal getty program for virtual terminals
Name: mingetty
Version: 1.08
Release: 2%{?dist}
License: GPLv2+
Group: System Environment/Base
URL: http://sourceforge.net/projects/mingetty/
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha1 mingetty=283acd3dc9da2c9eb71d5d7cc01d1bd178254523
Vendor:		VMware, Inc.
Distribution:	Photon

%description
The mingetty program is a lightweight, minimalist getty program for
use only on virtual terminals

%prep
%setup -q

%build
%global _hardened_build 1
make "CFLAGS=-Wall -D_GNU_SOURCE"

%install
install -d %{buildroot}/{sbin,%{_mandir}/man8}
install -m 0755 mingetty %{buildroot}/sbin/
install -m 0644 mingetty.8 %{buildroot}/%{_mandir}/man8/

%files
%doc COPYING
/sbin/mingetty
%{_mandir}/man8/mingetty.*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  1.08-2
-	GA - Bump release of all rpms
*	Mon Nov 30 2015 Anish Swaminathan <anishs@vmware.com> 1.08-1
-	Initial build. First version
