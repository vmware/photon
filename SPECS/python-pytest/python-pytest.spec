Name:           python3-pytest
Version:        7.1.2
Release:        3%{?dist}
Summary:        pytest is a mature full-featured Python testing tool that helps you write better programs
Group:          Development/Languages/Python
URL:            https://docs.pytest.org
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/4b/24/7d1f2d2537de114bdf1e6875115113ca80091520948d370c964b88070af2/pytest-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-attrs
BuildRequires:  python3-iniconfig
BuildRequires:  python3-more-itertools
BuildRequires:  python3-packaging
BuildRequires:  python3-pluggy
BuildRequires:  python3-py
BuildRequires:  python3-toml
BuildRequires:  python3-typing-extensions
BuildRequires:  python3-pip
BuildRequires:  python3-wcwidth

Requires:       python3
Requires:       python3-pluggy
Requires:       python3-iniconfig
Requires:       python3-packaging
Requires:       python3-toml
Requires:       python3-attrs
Requires:       python3-py
Requires:       python3-setuptools

BuildArch:      noarch

%description
pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.

%prep
%autosetup -p1 -n pytest-%{version}

%build
%py3_build

%install
%py3_install
mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest%{python3_version}
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest3
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest-%{python3_version}
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test%{python3_version}
ln -snf py.test%{python3_version} %{buildroot}%{_bindir}/py.test3

%if 0%{?with_check}
%check
make %{_smp_mflags} check
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/pytest*
%{_bindir}/py.test*
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.1.2-3
- Release bump for SRP compliance
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.1.2-2
- Use system provided packages to do offline build
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 7.1.2-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 6.2.5-1
- Upgrade to 6.2.5 which is python3.10 compatible
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 6.1.2-2
- Fix build with new rpm
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 6.1.2-1
- Automatic Version Bump
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 6.1.0-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.2-1
- Automatic Version Bump
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.4.3-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 3.8.2-2
- Mass removal python2
* Tue Oct 09 2018 Tapas Kundu <tkundu@vmware.com> 3.8.2-1
- Updated to release 3.8.2
- Removed buildrequires from subpackage.
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.7-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0.7-2
- Use python2 instead of python and rename the scripts in bin directory
* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0.7-1
- Initial
