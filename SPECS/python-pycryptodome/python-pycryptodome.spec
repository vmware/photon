Summary:        Cryptographic library for Python
Name:           python3-pycryptodome
Version:        3.12.0
Release:        1%{?dist}
License:        BSD and Public Domain
URL:            http://www.pycryptodome.org/
Source0:        pycryptodome-%{version}.tar.gz
%define sha512  pycryptodome=67f2a814d74305614fdf9dfb633c4fd9d80d2064119d0ecab24ae52fd8ce4b6de1a1e82c6ba7bcf22fb7db1a5a850adf078e22317b4c07229cd7cb8cb7f1ffd4
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-tools
Requires:       python3
Provides:       python3-pycrypto

%description
PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.

%prep
%autosetup -p1 -n pycryptodome-%{version}

%build
%py3_build

%install
python3 setup.py install --root=%{buildroot} --prefix=%{_prefix}

%check
python3 setup.py test

%files
%defattr(-, root, root,-)
%{python3_sitelib}/*

%changelog
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.12.0-1
- Initial Build pycryptodome
