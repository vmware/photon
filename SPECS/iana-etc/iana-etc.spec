Summary:        Data for network services and protocols
Name:           iana-etc
Version:        2.30
Release:        3%{?dist}
URL:            http://freshmeat.net/projects/iana-etc
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
Source0:        http://anduin.linuxfromscratch.org/sources/LFS/lfs-packages/conglomeration//iana-etc/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}
%description
The Iana-Etc package provides data for network services and protocols.
%prep
%autosetup -p1
%build
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%config %_sysconfdir/protocols
%config %_sysconfdir/services
%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.30-3
- Release bump for SRP compliance
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.30-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.30-1
- Initial build. First version
