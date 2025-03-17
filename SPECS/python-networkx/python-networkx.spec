%define srcname networkx

Name:           python3-networkx
Version:        3.2
Release:        2%{?dist}
Summary:        Creates and Manipulates Graphs and Networks
URL:            https://networkx.org
Vendor:         VMware, Inc.
Group:          Development/Languages/Python
Distribution:   Photon

Source0: https://github.com/networkx/networkx/archive/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

Requires: python3

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
BuildRequires: python3-pip
BuildRequires: python3-pytest

%description
NetworkX is a Python package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
pip3 install tomli
%{pytest}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.2-2
- Release bump for SRP compliance
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.2-1
- Initial version. Needed by selinux-python.
