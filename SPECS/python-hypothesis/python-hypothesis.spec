Name:           python3-hypothesis
Version:        6.54.4
Release:        2%{?dist}
Summary:        Python library for creating unit tests which are simpler to write and more powerful
Group:          Development/Languages/Python
Url:            https://github.com/HypothesisWorks/hypothesis-python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: https://pypi.python.org/packages/cf/d5/b3d491e4b5094be0ef69b910d637096c8e23f84a9bdc4eba0b869220d1f0/hypothesis-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-sortedcontainers
BuildRequires:  python3-attrs

Requires:       python3
Requires:       python3-sortedcontainers

BuildArch:      noarch

%description
Hypothesis is an advanced testing library for Python. It lets you write tests which are parametrized by a source of examples,
and then generates simple and comprehensible examples that make your tests fail. This lets you find more bugs in your code with less work

%prep
%autosetup -p1 -n hypothesis-%{version}

%build
%py3_build

%install
%py3_install

%check
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/hypothesis

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.54.4-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 6.54.4-1
- Automatic Version Bump
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 5.41.1-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 5.41.1-1
- Automatic Version Bump
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 5.36.1-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 5.36.0-1
- Automatic Version Bump
* Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 5.34.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 5.33.2-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 5.30.0-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 5.29.0-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 5.24.2-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.23.2-1
- Automatic Version Bump
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 3.71.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.71.0-1
- Update to version 3.71.0
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.8.2-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.8.2-2
- Changed python to python2
* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.8.2-1
- Initial
