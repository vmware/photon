Name:           python3-hatch-fancy-pypi-readme
Version:        22.8.0
Release:        1%{?dist}
Summary:        Fancy PyPI READMEs with Hatch
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/hynek/hatch-fancy-pypi-readme
Source0:        https://files.pythonhosted.org/packages/source/h/hatch-fancy-pypi-readme/hatch_fancy_pypi_readme-%{version}.tar.gz
%define sha512  hatch_fancy_pypi_readme=e8f28a9020fc38bb03187e85688531c0fa895fcc56f3deb241bf19a71b2e88f2a354526eabe1a8e0bf7736f97883208eec2a7eac4199e08ddc40988643491632
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy

Requires:       python3

%description
hatch-fancy-pypi-readme is a Hatch metadata plugin for everyone who cares about
the first impression of their project’s PyPI landing page. It allows you to
define your PyPI project description in terms of concatenated fragments that
are based on static strings, files, and most importantly: parts of files
defined using cut-off points or regular expressions.

%prep
%autosetup -n hatch_fancy_pypi_readme-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{_bindir}/hatch-fancy-pypi-readme
%{python3_sitelib}/*

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 22.8.0-1
- Initial version
