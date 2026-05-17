%global build_if %{photon_subrelease} >= 91

%define srcname flit_core

Name:           python3-flit-core
Version:        3.12.0
Release:        3%{?dist}
Summary:        The build backend used by Hatch
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/flit_core

BuildArch:      noarch

Source0:        https://files.pythonhosted.org/packages/source/f/flit_core/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel

%define ExtraBUildRequires python3-pip

Requires:       python3

%description
This is the extensible, standards compliant build backend used by Hatch.

%prep
%autosetup -n %{srcname}-%{version}

%build
python3 -m ensurepip
%{pyproject_wheel}

%install
%{pyproject_install}

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.12.0-3
- Extended to build for subrelease 91 and above
* Mon Mar 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.12.0-2
- Fix BuildRequires
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.12.0-1
- Upgrade to 3.12.0 for compatiblity with python 3.14
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.7.1-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.7.1-1
- Initial version
