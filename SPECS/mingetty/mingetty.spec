Summary:        A minimal getty program for virtual terminals
Name:           mingetty
Version:        1.08
Release:        3%{?dist}
License:        GPLv2+
Group:          System Environment/Base
URL:            http://sourceforge.net/projects/mingetty
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha512  %{name}=d2c050a412af81d4635cbaa5610dfa2cf2addce0d3116fa53f73eb15cd6b53d476165a0509ae630a151de07a5bdc82cba1b5da0ab78d0313b200adece3c8872b

%description
The mingetty program is a lightweight, minimalist getty program for
use only on virtual terminals

%prep
%autosetup -p1

%build
export CFLAGS="-Wall -D_GNU_SOURCE"
%make_build

%install
mkdir -p %{buildroot}/{%{_sbindir},%{_mandir}/man8}
%make_install %{?_smp_mflags} SBINDIR=%{_sbindir}

%files
%doc COPYING
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.*

%changelog
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.08-3
- Fix binary path
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.08-2
- GA - Bump release of all rpms
* Mon Nov 30 2015 Anish Swaminathan <anishs@vmware.com> 1.08-1
- Initial build. First version
