Summary:    List Open Files
Name:       lsof
Version:    4.96.4
Release:    2%{?dist}
URL:        https://people.freebsd.org/~abe
Group:      System Environment/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/lsof-org/lsof/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=06f8005e1eb72324c1fd603d8b8287a61ad6fdec182e9da833991a8915aaa69c416af1564d3b1087cb08b3504ef9b15cdffec7051605e89d945d6750ec8da985

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libtirpc-devel

Requires:   libtirpc

%description
Contains programs for generating Makefiles for use with Autoconf.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
./Configure -n linux
make CFGL="-L./lib -ltirpc" %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_sbindir} \
         %{buildroot}%{_mandir}/man8

install -v -m 0755 lsof %{buildroot}%{_sbindir}
install -v -m 0644 Lsof.8 %{buildroot}%{_mandir}/man8

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 4.96.4-2
- Release bump for SRP compliance
* Mon Dec 19 2022 Susant Sahani <ssahani@vmware.com> 4.96.4-1
- Bump version
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.95.0-2
- Bump version as a part of libtirpc upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 4.95.0-1
- Automatic Version Bump
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.91-1
- Update to version 4.91
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.89-2
- GA - Bump release of all rpms
* Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 4.89-1
- Initial build.
