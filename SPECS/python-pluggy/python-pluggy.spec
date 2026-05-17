%global build_if %{photon_subrelease} >= 91

Name:           python3-pluggy
Version:        1.6.0
Release:        2%{?dist}
Summary:        The plugin manager stripped of pytest specific details
Group:          Development/Libraries
URL:            https://pypi.org/project/pluggy/
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0:        https://files.pythonhosted.org/packages/f8/04/7a8542bed4b16a65c2714bf76cf5a0b026157da7f75e87cc88774aa10b14/pluggy-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel
BuildRequires:  python3-typing-extensions

Requires:       python3

Provides:       python3dist(pluggy) = %{version}-%{release}
Provides:       python%{python3_version}dist(pluggy) = %{version}-%{release}

%description
The plugin manager stripped of pytest specific details.

%prep
%autosetup -p1 -n pluggy-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.6.0-2
- Extended to build for subrelease 91 and above
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6.0-1
- Version upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.0-3
- Release bump for SRP compliance
* Fri Jul 19 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 1.0.0-2
- Use system provided packages to do offline build
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.0-1
- Automatic Version Bump
* Sun Sep 20 2020 Susant Sahani <ssahani@vmware.com> 0.13.1-1
- Initial rpm release
