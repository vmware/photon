%global build_if %{photon_subrelease} >= 91

Summary:        Cryptographic library for Python
Name:           python3-pycryptodome
Version:        3.20.0
Release:        4%{?dist}
URL:            http://www.pycryptodome.org/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/b9/ed/19223a0a0186b8a91ebbdd2852865839237a21c74f1fbc4b8d5b62965239/pycryptodome-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel

Requires:       python3

Provides:       python3-pycrypto
Obsoletes:      python3-pycrypto

%description
PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.

%prep
%autosetup -p1 -n pycryptodome-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-, root, root,-)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.20.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.20.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.20.0-2
- Release bump for SRP compliance
* Mon Apr 15 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.20.0-1
- Update to 3.20.0, fixes CVE-2023-52323
* Mon Dec 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.12.0-2
- Add Obsolete pycrypto
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.12.0-1
- Initial Build pycryptodome
