Summary:        World timezone definitions, modern and historical
Name:           python3-pytz
Version:        2022.2.1
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/pytz
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/pytz/pytz-%{version}.tar.gz
%define sha512  pytz=9c78d9f484e2e0e101ca7e10fba8e6c9870255b2c320b3499a0cc9b480adac64b07f2f124048aa957c6bc9311a4ac43060368e1f0d85d8e8c8f7df598e47912b
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  unzip

%if %{with_check}
BuildRequires: python3-setuptools
BuildRequires: python3-xml
BuildRequires: python3-pytest
%endif

Requires:       python3
Requires:       python3-libs
Requires:       tzdata

%description
pytz brings the Olson tz database into Python. This library allows
accurate and cross platform timezone calculations using Python 2.4
or higher. It also solves the issue of ambiguous times at the end
of daylight saving time, which you can read more about in the Python
Library Reference (``datetime.tzinfo``).

%prep
%autosetup -n pytz-%{version}

%build
%py3_build

%install
%py3_install

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    py.test%{python3_version} -v

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2022.2.1-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2022.2.1-1
- Automatic Version Bump
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 2020.4-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 2020.4-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2020.1-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 2018.5-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2018.5-1
- Update to version 2018.5
* Fri Aug 18 2017 Rongrong Qiu <rqiu@vmware.com> 2017.2-3
- add BuildRequires for make check bug 1937039
* Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 2017.2-2
- Requires tzdata
* Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 2017.2-1
- Initial packaging for Photon
