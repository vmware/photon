Summary:        Data for network services and protocols
Name:           iana-etc
Version:        20250711
Release:        1%{?dist}
License:        MIT
URL:            https://www.iana.org/protocols
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://github.com/Mic92/iana-etc/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=dae7d23d03e33766071bcacc7e6fa2f4c3d3ee87554ca34b1004257731b30556bce314ebb189e8352e32b67d0f819d45178627ad5873401924ddd6a02dbca96f

Patch0: 0001-add-pseudo-protocol-number-for-ip.patch

%description
The Iana-Etc package provides data for network services and protocols.
/etc/protocols and /etc/services provided by IANA

%prep
%autosetup -p1

%build
# remove trailing spaces from the files
sed -i 's/[[:space:]]*$//' protocols
sed -i 's/[[:space:]]*$//' services

%install
install -vDm644 protocols %{buildroot}%{_sysconfdir}/protocols
install -vDm644 services %{buildroot}%{_sysconfdir}/services

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/protocols
%config(noreplace) %{_sysconfdir}/services

%changelog
* Thu Jul 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20250711-1
- Update to latest protocols, services
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.30-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.30-1
- Initial build. First version
