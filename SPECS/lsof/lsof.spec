Summary:        List Open Files
Name:           lsof
Version:        4.91
Release:        2%{?dist}
License:        BSD
URL:            https://people.freebsd.org/~abe/
Group:          System Environment/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://fossies.org/linux/misc/%{name}_%{version}.tar.bz2
Patch0:         crash-fix-for-print-endpoint-unaccepted-socket-with-E-option.patch
%define sha512  %{name}=49f811941dd6303f7cb0655fddb8b1177af5d1b18f2bd1edfab09d2c128aea73daecf09c7a5375979c66ba764c88a6e70c9086b55c3634e3be01ab1aa12e9f92
BuildRequires:	libtirpc-devel
Requires:	libtirpc

%description
Contains programs for generating Makefiles for use with Autoconf.

%prep
# Using autosetup is not feasible
%setup -q -n %{name}_%{version}
tar -xf %{name}_%{version}_src.tar
cd %{name}_%{version}_src
%patch0 -p1

%build
cd %{name}_%{version}_src
./Configure -n linux
make CFGL="-L./lib -ltirpc" %{?_smp_mflags}

%install
cd %{name}_%{version}_src
mkdir -p %{buildroot}%{_sbindir}
install -v -m 0755 lsof %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
install -v -m 0644 lsof.8 %{buildroot}%{_mandir}/man8

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Wed Jul 27 2022 Nitesh Kumar <kunitesh@vmware.com> 4.91-2
- Patched to fix lsof+E crash
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.91-1
- Update to version 4.91
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.89-2
- GA - Bump release of all rpms
* Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 4.89-1
- Initial build.
