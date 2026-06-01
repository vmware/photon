%global build_if %{photon_subrelease} <= 90

Summary:        Data for network services and protocols
Name:           iana-etc
Version:        20250711
Release:        1.1%{?dist}
URL:            https://www.iana.org/protocols
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://github.com/Mic92/iana-etc/releases/download/%{version}/%{name}-%{version}.tar.gz

Source2: license.txt
%include %{SOURCE2}

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
* Mon Jun 01 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 20250711-1.1
- Move to SPECS/90
* Thu Jul 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 20250711-1
- Update to latest protocols, services
* Tue Jun 17 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.30-4
- Release bump for aarch64 SRP compliance
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.30-3
- Release bump for SRP compliance
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.30-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.30-1
- Initial build. First version
