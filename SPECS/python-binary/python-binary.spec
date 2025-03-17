Name:           python3-binary
Version:        1.0.0
Release:        3%{?dist}
Summary:        Library to convert between binary and SI units
Group:          Development/Languages/Python
Url:            https://github.com/ofek/binary
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/b/binary/binary-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-six
BuildRequires:  python3-attrs
%endif
Requires:       python3

BuildArch:      noarch

%description
Binary provides a bug-free and easy way to convert between and within binary (IEC) and decimal (SI) units.

%prep
%autosetup -n binary-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pluggy atomicwrites more_itertools
python3 -m pytest tests

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.0-3
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.0-2
- Update release to compile with python 3.11
* Tue Sep 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.0-1
- Initial Build
