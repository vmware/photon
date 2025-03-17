Name:           python3-nocaselist
Version:        1.0.6
Release:        3%{?dist}
Summary:        A case-insensitive list for Python
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/fe/5c/bfb5a421027852e577491ebfa6f9e454066bd430b4b7007692776c45da62/nocaselist-1.0.4.tar.gz
Source0:        nocaselist-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.6-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.6-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.6-1
- Automatic Version Bump
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.0.4-1
- Initial packaging for python3-nocaselist
