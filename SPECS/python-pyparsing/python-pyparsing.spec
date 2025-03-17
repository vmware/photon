Summary:        Python parsing module.
Name:           python3-pyparsing
Version:        3.0.9
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/pyparsing/%{version}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        pyparsing-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core

Requires:       python3
Requires:       python3-libs

%description
Python parsing module.

%prep
%autosetup -p1 -n pyparsing-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

#%%check
#Tests are not available

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.0.9-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.0.9-1
- Update to version 3.0.9
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.7-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.2.0-4
- Mass removal python2
* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 2.2.0-3
- Disabled check section as tests are not available
* Tue Jun 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.0-2
- Add build dependency with python-setuptools to handle 1.0 update
* Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 2.2.0-1
- Update to 2.2.0 and remove build dependency with python-setuptools
* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.10-1
- Initial packaging for Photon
