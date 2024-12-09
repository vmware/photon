Name:           python3-appdirs
Version:        1.4.4
Release:        4%{?dist}
Summary:        Python 2 and 3 compatibility utilities
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/appdirs

Source0: https://pypi.python.org/packages/48/69/d87c60746b393309ca30761f8e2b49473d43450b150cb08f3c6df5c11be5/appdirs-%{version}.tar.gz
%define sha512 appdirs=8b0cdd9fd471d45b186aa47607691cf378dabd3edc7b7026a57bd6d6f57698e86f440818a5e23ba4288b35d6bb8cb6eb0106eae8aab09d8863ee15025d300883

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
Requires:       python3

BuildArch:      noarch

Provides:       python%{python3_version}dist(appdirs) = %{version}

%description
A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".

%prep
%autosetup -p1 -n appdirs-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
pushd test
export PATH=%{buildroot}%{_bindir}:${PATH}
export PYTHONPATH=%{buildroot}%{python3_sitelib}
python3 test_api.py
popd
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.4-4
- Release bump for SRP compliance
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.4-3
- Update release to compile with python 3.11
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.4.4-2
- Fix build with new rpm
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.4-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 1.4.3-4
- Mass removal python2
* Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.3-3
- Changes to check section
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.3-2
- Change python to python2
* Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 1.4.3-1
- Create appdirs 1.4.3
