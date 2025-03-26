Name:           python3-flit-core
Version:        3.7.1
Release:        2%{?dist}
Summary:        The build backend used by Hatch
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/flit_core/
Source0:        https://files.pythonhosted.org/packages/source/f/flit_core/flit_core-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pip
BuildArch:      noarch

%description
This is the extensible, standards compliant build backend used by Hatch.

%prep
%autosetup -n flit_core-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.7.1-2
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.7.1-1
- Initial version
