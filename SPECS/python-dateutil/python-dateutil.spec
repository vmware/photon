Summary:        Extensions to the standard Python datetime module
Name:           python3-dateutil
Version:        2.8.2
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/python-dateutil
Source0:        https://pypi.python.org/packages/54/bb/f1db86504f7a49e1d9b9301531181b00a1c7325dc85a29160ee3eaa73a54/python-dateutil-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml
BuildRequires:  python3-typing-extensions
Requires:       python3
Requires:       python3-libs
Requires:       python3-six
BuildArch:      noarch
Provides:       python%{python3_version}dist(dateutil)

%description
The dateutil module provides powerful extensions to the datetime module available in the Python standard library.

%prep
%autosetup -n python-dateutil-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.2-3
- Release bump for SRP compliance
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.2-2
- Add typing-extensions in BuildRequires
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.8.2-1
- Automatic Version Bump
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 2.8.1-2
- Added provides
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8.1-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 2.7.3-2
- Mass removal python2
* Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 2.7.3-1
- Updated to release 2.7.3
* Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> 2.6.1-1
- Initial packaging for photon.
