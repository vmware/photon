Name:           python3-more-itertools
Version:        8.14.0
Release:        2%{?dist}
Summary:        More routines for operating on Python iterables, beyond itertools
Group:          Development/Libraries
URL:            https://github.com/erikrose/more-itertools
Source0:        https://files.pythonhosted.org/packages/d6/03/37d7c431c4c1c17507fb7b89240ddb7be70f2027277960d525f1679363c1/more-itertools-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

Requires:       python3

Provides:       python3dist(more-itertools) = %{version}-%{release}
Provides:       python%{python3_version}dist(more-itertools) = %{version}-%{release}

%description
Python's itertools library is a gem - you can compose elegant solutions for
a variety of problems with the functions it provides. In more-itertools we
collect additional building blocks, recipes, and routines for working with
Python iterables

%prep
%autosetup -n more-itertools-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 8.14.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 8.14.0-1
- Automatic Version Bump
* Sun Sep 20 2020 Susant Sahani <ssahani@vmware.com> 8.5.0-1
- Initial rpm release
