Name:           python3-semantic-version
Version:        2.10.0
Release:        1%{?dist}
Summary:        Library implementing the 'SemVer' scheme
License:        BSD-2-Clause
Group:          Development/Languages/Python
Url:            https://github.com/rbarrois/python-semanticversion
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/7d/31/f2289ce78b9b473d582568c234e104d2a342fd658cc288a7553d83bb8595/semantic_version-%{version}.tar.gz
%define sha512  semantic_version=869a3901d4fc12acb285c94175011ed03dc00b35ab687c67dda458cffab5666cea21bc1b4bf75ef4edeb83b8080452a1c1470248eee54bbd269614a8cab132dc

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing-extensions
%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

%description
This small python library provides a few tools to handle SemVer in Python.
It follows strictly the 2.0.0 version of the SemVer scheme.

%prep
%autosetup -n semantic_version-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pluggy atomicwrites more_itertools
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.10.0-1
- Initial Build
