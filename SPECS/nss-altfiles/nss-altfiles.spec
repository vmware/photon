Summary:    NSS module to read passwd/group files from alternate locations
Name:       nss-altfiles
Version:    2.23.0
Release:    2%{?dist}
URL:        https://github.com/aperezdc/nss-altfiles
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon

Source0:    https://github.com/aperezdc/nss-altfiles/archive/%{name}-%{version}.tar.gz
%define sha512 nss-altfiles=d4d6ff4eb416f63640119e678ec130476b7398d023f25ec18dc1992c4157b8d4c65a99be5d212532c30079f277ccb157567e86ca7347f05ebf317603631d5bca

Source1: license.txt
%include %{SOURCE1}

BuildRequires: glibc-devel

%description
NSS module to read passwd/group files from alternate locations.

%prep
%autosetup -p1

%build
export CFLAGS='%{optflags}'
%configure

%make_build

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md
%{_libdir}/*.so.*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.23.0-2
- Release bump for SRP compliance
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.23.0-1
- Update to 2.23.0
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.19.1-2
- GA - Bump release of all rpms
* Sat Jul 11 2015 Touseef Liaqat <tliaqat@vmware.com> 2.19.1-2
- Initial version
