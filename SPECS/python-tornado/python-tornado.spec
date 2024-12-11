Name:           python3-tornado
Version:        6.2
Release:        3%{?dist}
Summary:        Tornado is a Python web framework and asynchronous networking library
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/tornado
Source0:        https://pypi.python.org/packages/fa/14/52e2072197dd0e63589e875ebf5984c91a027121262aa08f71a49b958359/tornado-%{version}.tar.gz
%define sha512  tornado=157cbeee21bef29ac68b319329e7fc57db4c68dbb5a245e2171b7a28427ebbfe16b745e3bdbdec5912caae5eaa60c3cbbf8830c9c76fec5ffdf025e234468517

Source1: license.txt
%include %{SOURCE1}

Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3 python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description
Tornado is a Python web framework and asynchronous networking library

%prep
%autosetup -n tornado-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.2-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 6.2-2
- Update release to compile with python 3.11
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 6.2-1
- Automatic Version Bump
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 6.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.4-1
- Automatic Version Bump
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 4.5.2-3
- Mass removal python2
* Tue Dec 17 2019 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-2
- To build python2 and python3 tornado packages
- To remove buildArch
* Mon Dec 11 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-1
- Initial version of python tornado for PhotonOS.
