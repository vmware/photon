%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        iniconfig: brain-dead simple config-ini parsing
Name:           python3-iniconfig
Version:        1.1.1
Release:        1%{?dist}
License:        MIT
URL:            http://github.com/RonnyPfannschmidt/iniconfig
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/23/a2/97899f6bd0e873fed3a7e67ae8d3a08b21799430fb4da15cfedf10d6e2c2/iniconfig-%{version}.tar.gz
%define sha1    iniconfig-%{version}=f0d3a75f00752f75876468d04bf0cfbc05643b7e

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides:       python3.9dist(iniconfig) = %{version}

%description
iniconfig is a small and simple INI-file parser module having a unique set of features:

1. tested against Python2.4 across to Python3.2, Jython, PyPy
2. maintains order of sections and entries
3. supports multi-line values with or without line-continuations
4. supports “#” comments everywhere
5. raises errors with proper line-numbers
6. no bells and whistles like automatic substitutions
7. iniconfig raises an Error if two sections have the same name.

%prep
%autosetup -n iniconfig-%{version}

%install
python3 setup.py install --skip-build --root %{buildroot}

%post
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/iniconfig*.egg-info/*

%changelog
*   Tue Nov 10 2020 Susant Sahani <ssahani@vmware.com> 1.1.1-1
-   Initial rpm release.
