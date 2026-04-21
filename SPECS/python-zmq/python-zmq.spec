%global build_if %{photon_subrelease} >= 92

Summary:        Software library for fast, message-based applications
Name:           python3-zmq
Version:        23.2.1
Release:        5%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pyzmq
Source0:        https://pypi.python.org/packages/af/37/8e0bf3800823bc247c36715a52e924e8f8fd5d1432f04b44b8cd7a5d7e55/pyzmq-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  zeromq-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools
BuildRequires:  cython3
Requires:       python3
Requires:       zeromq
Provides:       python%{python3_version}dist(pyzmq)

%description
python bindings for zeromq

%prep
%autosetup -n pyzmq-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root)
%doc README.md COPYING.* examples/
%{python3_sitelib}/pyzmq-*.egg-info
%{python3_sitelib}/zmq

%changelog
* Mon Apr 20 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 23.2.1-5
- Use photon specific libzmq
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 23.2.1-4
- Bump version as a part of python3.14 upgrade
* Tue Aug 12 2025 Bo Gan <bo.gan@broadcom.com> 23.2.1-3
- Cleanup and rescan licenses
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 23.2.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 23.2.1-1
- Automatic Version Bump
* Tue Jun 15 2021 Keerthana K <keerthanak@vmware.com> 19.0.2-2
- Added Provides: python3.9dist(pyzmq)
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 19.0.2-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 19.0.1-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 17.1.2-2
- Mass removal python2
* Thu Sep 20 2018 Tapas Kundu <tkundu@vmware.com> 17.1.2-1
- Updated to release 17.1.2
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-2
- Add python3-libs to BuildRequires
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.0.2-1
- Initial packaging for Photon
