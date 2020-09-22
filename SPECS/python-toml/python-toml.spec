%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-toml
Version:        0.10.1
Release:        1%{?dist}
Summary:        Python Library for Tom's Obvious, Minimal Language
Group:          Development/Libraries
License:        MIT
URL:            https://pypi.python.org/pypi/
Source0:        https://files.pythonhosted.org/packages/da/24/84d5c108e818ca294efe7c1ce237b42118643ce58a14d2462b3b2e3800d5/toml-0.10.1.tar.gz
%define sha1    toml=1e1de9572d86421f71f1c93a67b100031444eca3
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

Requires:       python3

Provides:       python3dist(toml) = %{version}
Provides:       python3.8dist(toml) = %{version}

%description
Python Library for Tom's Obvious, Minimal Language

%prep
%autosetup -p1 -n toml-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Sep 21 2020 Susant Sahani <ssahani@vmware.com> 0.10.1-1
- Initial rpm release
