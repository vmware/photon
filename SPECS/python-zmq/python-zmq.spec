Summary:        Software library for fast, message-based applications
Name:           python3-zmq
Version:        23.2.1
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pyzmq
Source0:        https://pypi.python.org/packages/af/37/8e0bf3800823bc247c36715a52e924e8f8fd5d1432f04b44b8cd7a5d7e55/pyzmq-%{version}.tar.gz
%define sha512  pyzmq=c8f2dc858076641a219ea37af91ad4a15ee811e8d2095b0337d414cc702eaf90ee4d6280bda7800667828dffaedcdb026553262d5473f9fb70bbd17c17b248f4

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools
BuildRequires:  cython3
Requires:       python3
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
