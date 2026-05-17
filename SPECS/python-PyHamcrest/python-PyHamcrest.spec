%global build_if %{photon_subrelease} >= 91

Name:           python3-PyHamcrest
Version:        2.0.2
Release:        5%{?dist}
Summary:        Python Hamcrest framework for matcher objects
Group:          Development/Libraries
URL:            https://pypi.org/project/PyHamcrest
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/n/deepmerge/PyHamcrest-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description
PyHamcrest is a framework for writing matcher objects, allowing you to declaratively define “match” rules.

%prep
%autosetup -n PyHamcrest-%{version}

%build
%py3_build

%install
%py3_install

%check
#no test folder in source tar

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%doc README.rst
%doc LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.0.2-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.2-4
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.2-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.2-2
- Update release to compile with python 3.11
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.9.0-2
- Mass removal python2
* Fri Aug 30 2019 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
- Initial packaging for photon OS
