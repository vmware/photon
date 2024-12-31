Name:           python3-tornado
Version:        6.0.4
Release:        4%{?dist}
Summary:        Tornado is a Python web framework and asynchronous networking library
License:        PSFL
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/tornado
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://pypi.python.org/packages/fa/14/52e2072197dd0e63589e875ebf5984c91a027121262aa08f71a49b958359/tornado-%{version}.tar.gz
%define sha512 tornado=d29d69cf40f8b34fb2c55d81b6ecd9bc7c6fdf644eb4ff35452829510c0d5ec185da0a6067fec3e8afb2bedf9f5f08b06adb0ad53dcab04cb791a75abc304d6e

Patch0: CVE-2024-52804.patch

BuildRequires:  python3-devel

Requires:       python3

%description
Tornado is a Python web framework and asynchronous networking library,
originally developed at FriendFeed.

%prep
%autosetup -p1 -n tornado-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Dec 30 2024 Prashant S Chauhan <prashant.singh-chauhan@bradcom.com> 6.0.4-4
- Fix CVE-2024-52804
* Tue Sep 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.0.4-3
- Add description
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 6.0.4-2
- Bump up to compile with python 3.10
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.4-1
- Automatic Version Bump
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 4.5.2-3
- Mass removal python2
* Tue Dec 17 2019 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-2
- To build python2 and python3 tornado packages
- To remove buildArch
* Mon Dec 11 2017 Padmini Thirumalachar <pthirumalachar@vmware.com> 4.5.2-1
- Initial version of python tornado for PhotonOS.
