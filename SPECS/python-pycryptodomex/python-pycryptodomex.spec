%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Cryptographic library for Python
Name:           python3-pycryptodomex
Version:        3.9.9
Release:        1%{?dist}
License:        BSD and Public Domain
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pycryptodomex
Source0:        pycryptodomex-%{version}.tar.gz
%define sha1	pycryptodomex=f628a2f34e73804b7779d51ead3be6176860b481

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-sphinx

Requires:  python3-sphinx
Requires:  python3-libs
Requires:  python3
Requires:  python3-setuptools

%description
Cryptographic library for Python

%prep
%setup -q -n pycryptodomex-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build

%files
%defattr(-,root,root,-)
%{python3_sitelib}/Cryptodome
%{python3_sitelib}/pycryptodomex-3.9.9-py3.7.egg-info

%changelog
*   Tue Jan 19 2021 Tapas Kundu <tkundu@vmware.com> 3.9.9-1
-   Initial packaging for Photon
