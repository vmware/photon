Summary:        Attributes without boilerplate.
Name:           python3-attrs
Version:        22.1.0
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/attrs
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: attrs-%{version}.tar.gz
%define sha512 attrs=447637bc82b31d565479e364869b996eaf7b67e526ad97f79ba1c27f287bbb25a2c40663e35437bc19037f605fac9322bd35f303f2769f0eb2ee673900551885

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-zope.interface
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif

Requires:       python3

Provides:       python3dist(attrs) = %{version}-%{release}
Provides:       python%{python3_version}dist(attrs) = %{version}-%{release}

%description
Attributes without boilerplate.

%prep
%autosetup -p1 -n attrs-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install hypothesis==4.38.0
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 22.1.0-3
- Bump version as a part of openssl upgrade
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 22.1.0-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 22.1.0-1
- Automatic Version Bump
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.3.0-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 20.3.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20.2.0-2
- openssl 1.1.1
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 20.2.0-1
- Automatic Version Bump
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 20.1.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 19.3.0-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 18.2.0-4
- Mass removal python2
* Thu Feb 27 2020 Tapas Kundu <tkundu@vmware.com> 18.2.0-3
- hypothesis 4.38.2 has requirement attrs>=19.2.0,
- but we have attrs 18.2.0 which is incompatible.
* Tue Nov 13 2018 Tapas Kundu <tkundu@vmware.com> 18.2.0-2
- Fixed the makecheck errors
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.2.0-1
- Update to version 18.2.0
* Thu Jul 06 2017 Chang Lee <changlee@vmware.com> 16.3.0-3
- Updated %check
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.3.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 16.3.0-1
- Initial packaging for Photon
