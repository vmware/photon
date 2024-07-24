%define srcname oauthlib

Summary:        An implementation of the OAuth request-signing logic
Name:           python3-oauthlib
Version:        3.2.2
Release:        1%{?dist}
License:        BSD
Url:            https://pypi.python.org/pypi/python-oauthlib/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/6d/fa/fbf4001037904031639e6bfbfc02badfc7e12f137a8afa254df6c4c8a670/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=c147b96e0ab0d1a8845f525e80831cfd04495134dd1f17fd95eac62f3a95c91e6dca9d38e34206537d77f3c12dd5b553252239318ba39546979c350e96536b8b

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  libffi-devel

Requires:       python3

BuildArch:      noarch

%description
OAuthLib is a generic utility which implements the logic of OAuth without assuming a specific HTTP request object or web framework

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
pip3 install jwt
%{python3} setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}.dist-info/

%changelog
* Wed Jul 24 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.2.2-1
- Upgrade to v3.2.2
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.2.0-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.1.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.1.0-1
- Update to version 2.1.0
* Fri Jul 07 2017 Chang Lee <changlee@vmware.com> 2.0.2-3
- Add  libffi-devel in BuildRequires and install mock python module in %check
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.2-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Apr 13 2017 Anish Swaminathan <anishs@vmware.com> 2.0.2-1
- Initial packaging for Photon
