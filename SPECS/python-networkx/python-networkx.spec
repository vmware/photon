%define srcname networkx

Name:           python3-networkx
Version:        3.2
Release:        1%{?dist}
Summary:        Creates and Manipulates Graphs and Networks
License:        BSD-3-Clause
URL:            https://networkx.org
Vendor:         VMware, Inc.
Group:          Development/Languages/Python
Distribution:   Photon

Source0: https://github.com/networkx/networkx/archive/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=f9fdfbe0c716c5cc6cf3f47b44e02bbd8a166724c2ef7044497b01baf468f354123aeac3c032e31293c7eedd762a29f89628cbe2ecfea280cf6012d7b0d9bdfe

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
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.2-1
- Initial version. Needed by selinux-python.
