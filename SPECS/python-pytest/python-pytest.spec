%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Name:           python3-pytest
Version:        6.0.2
Release:        1%{?dist}
Summary:        pytest is a mature full-featured Python testing tool that helps you write better programs
License:        MIT
Group:          Development/Languages/Python
URL:            https://docs.pytest.org
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/00/e9/f77dcd80bdb2e52760f38dbd904016da018ab4373898945da744e5e892e9/pytest-%{version}.tar.gz
%define sha1    pytest=bc14d7c0f9c0a8299ffdc5a7c0bec1563b4052ac

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildRequires:  python3-attrs
BuildRequires:  python3-iniconfig
BuildRequires:  python3-more-itertools
BuildRequires:  python3-packaging
BuildRequires:  python3-pluggy >= 0.12
BuildRequires:  python3-py >= 1.5.0
BuildRequires:  python3-toml
BuildRequires:  python3-wcwidth

Requires:       python3-attrs
Requires:       python3-iniconfig
Requires:       python3-more-itertools
Requires:       python3-packaging
Requires:       python3-pluggy >= 0.12
Requires:       python3-py >= 1.5.0
Requires:       python3-toml
Requires:       python3-wcwidth
Requires:       python3
Requires:       python3-libs
Requires:       python3-py

BuildArch:      noarch

%description
pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.

%prep
%setup -n pytest-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest%{python3_version}
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest3
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test%{python3_version}
ln -snf py.test%{python3_version} %{buildroot}%{_bindir}/py.test3

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root,-)
%{_bindir}/pytest3
%{_bindir}/pytest%{python3_version}
%{_bindir}/py.test3
%{_bindir}/py.test%{python3_version}
%{python3_sitelib}/*

%changelog
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.2-1
-   Automatic Version Bump
*   Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.4.3-1
-   Automatic Version Bump
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 3.8.2-2
-   Mass removal python2
*   Tue Oct 09 2018 Tapas Kundu <tkundu@vmware.com> 3.8.2-1
-   Updated to release 3.8.2
-   Removed buildrequires from subpackage.
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.7-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0.7-2
-   Use python2 instead of python and rename the scripts in bin directory
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0.7-1
-   Initial
