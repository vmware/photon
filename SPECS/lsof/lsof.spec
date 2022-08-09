Summary:        List Open Files
Name:           lsof
Version:        4.95.0
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/lsof-org/lsof
Group:          System Environment/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/lsof-org/lsof/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=09c5c4b0ea0530e23b98b96df8485f37c2594028b604097a816aee216a8b1a7bc887071e8727cbaf3c765d0992314a5aa49723572cfe926f88806be18a6b8aef

BuildRequires:	libtirpc-devel
Requires:	libtirpc

%description
Contains programs for generating Makefiles for use with Autoconf.

%prep
%autosetup -n %{name}-%{version}

%build
./Configure -n linux
make CFGL="-L./lib -ltirpc" %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_sbindir}
install -v -m 0755 lsof %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
install -v -m 0644 Lsof.8 %{buildroot}%{_mandir}/man8

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Tue Aug 09 2022 Nitesh Kumar <kunitesh@vmware.com> 4.95.0-1
- Upgrade to v4.95.0 to fix a crash for unaccepted connection
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.91-1
- Update to version 4.91
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.89-2
- GA - Bump release of all rpms
* Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 4.89-1
- Initial build.
