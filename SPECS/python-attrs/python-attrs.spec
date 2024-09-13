Summary:        Attributes without boilerplate.
Name:           python3-attrs
Version:        22.2.0
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/attrs
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/21/31/3f468da74c7de4fcf9b25591e682856389b3400b4b62f201e65f15ea3e07/attrs-%{version}.tar.gz
%define sha512  attrs=a7707fb11e21cddd2b25c94c9859dc8306745f0256237493a4ad818ffaf005d1c1e84d55d07fce14eaea18fde4994363227286df2751523e1fe4ef6623562a20

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-zope.interface
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs

Provides:       python3dist(attrs) = %{version}-%{release}
Provides:       python%{python3_version}dist(attrs) = %{version}-%{release}

%description
Attributes without boilerplate.

%prep
%autosetup -p1 -n attrs-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
#python2 does not support for tests
pip3 install pytest hypothesis==4.38.0
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Sep 13 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 22.2.0-1
- Updating to v22.2.0 to make it compatible with python3-Twisted-22.10.0
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 20.3.0-3
- Update release to compile with python 3.10
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
