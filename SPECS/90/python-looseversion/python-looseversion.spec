%global build_if %{photon_subrelease} <= 90

Summary:        Version numbering for anarchists and software realists
Name:           python3-looseversion
Version:        1.3.0
Release:        2.1.1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/effigies/looseversion

Source0:        https://files.pythonhosted.org/packages/64/7e/f13dc08e0712cc2eac8e56c7909ce2ac280dbffef2ffd87bd5277ce9d58b/looseversion-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-packaging

Requires:       python3

BuildArch:      noarch

%description
Version numbering for anarchists and software realists

%prep
%autosetup -p1 -n looseversion-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
pip3 install tox
tox

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.3.0-2.1.1
- Adjusted to build for subrelease 90
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.3.0-2.1
- Bump after moving to SPECS/91
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.3.0-2
- Release bump for SRP compliance
* Thu Apr 18 2024 Prafful Mehrotra <prafful.mehrotra@broadcom.com> 1.3.0-1
- Adding looseversion python package to Photon 5
