%global build_if %{photon_subrelease} >= 91

Name:           python3-roman-numerals
Version:        4.1.0
Release:        2%{?dist}
Summary:        Manipulate well-formed Roman numerals
URL:            https://github.com/AA-Turner/roman-numerals
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

Source0: roman_numerals-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core

Requires: python3

%description
This project provides utilities manipulating well-formed Roman numerals,
in various programming languages.

%prep
%autosetup -p1 -n roman_numerals-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.1.0-2
- Extended to build for subrelease 91 and above
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.1.0-1
- Initial version, needed by sphinx-9.x
