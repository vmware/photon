Name:           python3-nocaselist
Version:        1.0.6
Release:        2%{?dist}
Summary:        A case-insensitive list for Python
License:        Apache Software License (Apache Software License 2.0)
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/fe/5c/bfb5a421027852e577491ebfa6f9e454066bd430b4b7007692776c45da62/nocaselist-1.0.4.tar.gz
Source0:        nocaselist-%{version}.tar.gz
%define sha512  nocaselist=1898bfda570450dd843fd07f25eb5abe1eed0e96be317b90b1f4b8dd847eeb6790f5deabf4f12228b932bf069f6fa6a73eeae1d6873aafe67f710a7bb47b6682
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch
Provides:       python%{python3_version}dist(nocaselist)

%description
A case-insensitive list for Python

%prep
%autosetup -n nocaselist-%{version}

%build
%py3_build

%install
%py3_install
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.6-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.6-1
- Automatic Version Bump
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.0.4-1
- Initial packaging for python3-nocaselist
