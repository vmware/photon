Summary:       A Python module for decorators, wrappers and monkey patching
Name:          python3-wrapt
Version:       1.14.1
Release:       1%{?dist}
Group:         Development/Tools/Python
License:       BSD
URL:           https://github.com/GrahamDumpleton/wrapt
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       https://files.pythonhosted.org/packages/11/eb/e06e77394d6cf09977d92bff310cb0392930c08a338f99af6066a5a98f92/wrapt-%{version}.tar.gz
%define sha512 wrapt=69986796303ad78f532b4f671829226c7bb43d97a494a111dcf397b68b447f64cee16d14d3f8c9eb84bbb9c1ac8709b6f33f7d78389b2968493e95ced63779ac

BuildRequires: gcc
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: python3

%description
The aim of the wrapt module is to provide a transparent object proxy for Python, which can be used as the basis for the construction
of function wrappers and decorator functions.

%prep
%autosetup -p1 -n wrapt-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root,-)
%doc README.rst
%license LICENSE
%{python3_sitearch}/wrapt
%{python3_sitearch}/wrapt-%{version}-py%{python3_version}.egg-info

%changelog
* Mon Aug 29 2022 Srish Srinivasan <ssrish@vmware.com> 1.14.1-1
- Initial build. First version