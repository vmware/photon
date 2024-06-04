Summary:        A pathlib-compatible Zipfile object wrapper.
Name:           python3-zipp
Version:        3.19.1
Release:        1%{?dist}
Url:            https://pypi.org/project/zipp/
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/4f/a1/ac66fba5917fb7860f91cb251ac6cf838923a8abe89e059cc1988cb256d1/zipp-%{version}.tar.gz
%define sha512  zipp=c0a4b4055f6652852526b7749d738cedda6534ea21945933ec727b5364a5558697fce6757e4045d30df55a1dce57509c92046f25d6914707fcc97e07f3088c3a

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%if 0%{?with_check}
BuildRequires:  python3-more-itertools
BuildRequires:  python3-pytest
BuildRequires:  python3-test
%endif

Requires:       python3

BuildArch:      noarch

Provides: python%{python3_version}dist(zipp)
Conflicts: python3-importlib-metadata < 6.0.0-2%{?dist}

%description
A pathlib-compatible Zipfile object wrapper. Official backport of the standard library Path object.

%prep
%autosetup -n zipp-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
pip3 install jaraco.itertools jaraco.functools jaraco.test
%{pytest} tests/
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.19.1-1
- Intial Build
