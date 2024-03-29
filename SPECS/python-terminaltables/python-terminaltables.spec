Summary:        Draw tables in terminal/console applications from a list of lists of strings
Name:           python3-terminaltables
Version:        3.1.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://robpol86.github.io/terminaltables/
Source0:        terminaltables-%{version}.tar.gz
%define sha512  terminaltables=dc49458652fff8bc6094d316d84c9b8e9fca1a26e3230c0b668bc03ec8528793f4ef024e8032d4a56fbfabfdfd4a1142870f550f0b373ba6a42dd2e3ead3f501
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-attrs
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif

Requires:       python3

%description
Easily draw tables in terminal/console applications from a list of lists of strings. Supports multi-line rows.

%prep
%autosetup -n terminaltables-%{version}

%build
%{py3_build}

%install
%{py3_install}

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
* Fri May 27 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.1.0-1
- Python terminaltables initial built
