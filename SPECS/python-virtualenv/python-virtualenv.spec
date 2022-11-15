Name:           python3-virtualenv
Version:        20.1.0
Release:        2%{?dist}
Summary:        Virtual Python Environment builder
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/virtualenv
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: virtualenv-%{version}.tar.gz
%define sha512 virtualenv=740bf8ba30d836c240d248dd2fa31a8702cfa8f96a6192dd6430dbeff3ebbf0fe67d4fd2439ed4961869731520b097783a29381eae3f81f6700b6050b75422c8

BuildRequires:  python3-devel
BuildRequires:  python3-appdirs
BuildRequires:  python3-setuptools
BuildRequires:  curl-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-appdirs
Requires:       python3-distlib
Requires:       python3-filelock

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

BuildArch:      noarch

%description
virtualenv is a tool to create isolated Python environment.

%prep
%autosetup -p1 -n virtualenv-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/virtualenv
%{python3_sitelib}/*

%changelog
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.1.0-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 20.1.0-1
- Automatic Version Bump
* Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.32-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.31-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.30-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.0.28-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 16.0.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 16.0.0-1
- Update to version 16.0.0
* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 15.1.0-1
- Initial version of python-virtualenv package for Photon.
