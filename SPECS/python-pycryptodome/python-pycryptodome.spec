Summary:        Cryptographic library for Python
Name:           python3-pycryptodome
Version:        3.12.0
Release:        1%{?dist}
License:        BSD and Public Domain
URL:            http://www.pycryptodome.org/
Source0:        pycryptodome-%{version}.tar.gz
%define sha1    pycryptodome=275fea97bb5ad686813bdab693bbc765c34a6abc
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-tools
Requires:       python3
%description
PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.

%prep
%autosetup -p1 -n pycryptodome-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --root=%{buildroot} --prefix=%{_prefix}

%check
python3 setup.py test

%files
%defattr(-, root, root,-)
%{python3_sitelib}/*

%changelog
*   Mon Jan 03 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.12.0-1
-   Initial Build pycryptodome
