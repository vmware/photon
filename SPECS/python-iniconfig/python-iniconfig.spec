Summary:        iniconfig: brain-dead simple config-ini parsing
Name:           python3-iniconfig
Version:        1.1.1
Release:        4%{?dist}
URL:            http://github.com/RonnyPfannschmidt/iniconfig
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/23/a2/97899f6bd0e873fed3a7e67ae8d3a08b21799430fb4da15cfedf10d6e2c2/iniconfig-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

Provides:       python%{python3_version}dist(iniconfig) = %{version}

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

%build
%py3_build

%install
%py3_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/iniconfig/*
%{python3_sitelib}/iniconfig*.egg-info/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.1.1-4
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.1.1-3
- Update release to compile with python 3.11
* Thu Aug 26 2021 Susant Sahani <ssahani@vmware.com> 1.1.1-2
- Use python macros
* Tue Nov 10 2020 Susant Sahani <ssahani@vmware.com> 1.1.1-1
- Initial rpm release.
