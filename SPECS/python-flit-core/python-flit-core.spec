Name:           python3-flit-core
Version:        3.9.0
Release:        1%{?dist}
Summary:        The build backend used by Hatch
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/flit_core

Source0:        https://files.pythonhosted.org/packages/source/f/flit_core/flit_core-%{version}.tar.gz
%define sha512  flit_core=1205589930d2c51d6aa6b2533a122a912e63b157e94adba2a0649a58d324fa98a5b84609d9b53e9d236f1cdb6a6984de2cefcf2f11abc2cd83956df21f269ad6

BuildRequires:  python3-devel
BuildRequires:  python3-pip

BuildArch:      noarch

Requires: python3

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
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.9.0-1
- Upgrade to v3.9.0
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.7.1-1
- Initial version
