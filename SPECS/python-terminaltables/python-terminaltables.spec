Summary:        Draw tables in terminal/console applications from a list of lists of strings
Name:           python3-terminaltables
Version:        3.1.10
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/matthewdeanmartin/terminaltables
Source0:        https://github.com/matthewdeanmartin/terminaltables/archive/terminaltables-%{version}.tar.gz
%define sha512  terminaltables=84fa403cee4206b6b19de0206d89535bd2965a0796e1890dd9b0a9c6593c5f41d0d24b88ee9db426067c777712a4e810d67d4d0246496239a7a96b53a24e8174

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
%if 0%{?with_check}
BuildRequires:  python3-attrs
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif

Requires:       python3

%description
Easily draw tables in terminal/console applications from a list of lists of strings. Supports multi-line rows.

%prep
%autosetup -n terminaltables-%{version}

%build
python3 -m pip wheel --disable-pip-version-check --verbose .

%install
python3 -m pip install --root %{buildroot} --prefix %{_prefix} --disable-pip-version-check --verbose .

%if 0%{?with_check}
%check
pip3 install funcsigs pathlib2 pluggy atomicwrites more_itertools colorama colorclass termcolor
python3 -m pytest tests
%endif

%files
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri May 27 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.1.10-1
- Python terminaltables initial build
