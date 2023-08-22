%define srcname platformdirs

Name:           python3-platformdirs
Version:        3.10.0
Release:        1%{?dist}
Summary:        Python module for determining appropriate platform-specific dirs
License:        MIT
URL:            https://github.com/platformdirs/platformdirs
Vendor:         VMware, Inc.
Group:          Development/Languages/Python
Distribution:   Photon

Source0: https://github.com/platformdirs/platformdirs/archive/refs/tags/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=39c068dad3fe6ec85247a8957c0fcfb27207e78041686a0231d836eeb431bba82583e2fcb609903bb0f479cd04e4c7866b6126e52a708e7e71eed7631bd121b0

BuildRequires: python3-devel
BuildRequires: python3-wheel
BuildRequires: python3-pip
BuildRequires: python3-hatchling
BuildRequires: python3-hatch-vcs
BuildRequires: python3-setuptools_scm
BuildRequires: python3-pathspec
BuildRequires: python3-pluggy
BuildRequires: python3-packaging

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-pip
BuildRequires: python3-appdirs
%endif

Requires: python3

BuildArch: noarch

%description
A small Python module for determining appropriate platform-specific dirs, e.g.
a "user data dir".

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
pip3 install tomli pytest-mock
%pytest -k "not test_compatibility"

%files
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Tue Aug 22 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.10.0-1
- New addtion. Needed by python3-virtualenv.
