Summary:        Cryptographic library for Python
Name:           python3-pycryptodome
Version:        3.20.0
Release:        1%{?dist}
License:        BSD and Public Domain
URL:            http://www.pycryptodome.org/
Source0: https://files.pythonhosted.org/packages/b9/ed/19223a0a0186b8a91ebbdd2852865839237a21c74f1fbc4b8d5b62965239/pycryptodome-%{version}.tar.gz
%define sha512 pycryptodome=9fed02190db9ae71b6895af2525d7670858817acf213c494969104da81138dacb11bc00be83b308e070a2c90766cd763e25a611ada402b32f6160a8ac9283f85
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-tools
Requires:       python3
Provides:       python3-pycrypto = 2.6.2
Obsoletes:      python3-pycrypto < 2.6.2

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
* Mon Apr 15 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.20.0-1
- Update to 3.20.0, fixes CVE-2023-52323
* Mon Jun 19 2023 Tapas Kundu <tkundu@vmware.com> 3.12.0-3
- Enhance provides and obsoletes of pycrypto
* Wed Jun 01 2022 Tapas Kundu <tkundu@vmware.com> 3.12.0-2
- Provides python3-pycrypto
* Mon Jan 03 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.12.0-1
- Initial Build pycryptodome
