Name:           python-pytest
Version:        3.8.2
Release:        2%{?dist}
Summary:        pytest is a mature full-featured Python testing tool that helps you write better programs
License:        MIT
Group:          Development/Languages/Python
URL:            https://docs.pytest.org
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pytest-dev/pytest/archive/refs/tags/pytest-%{version}.tar.gz
%define sha512 pytest=5420de07ff741f64bcb7fce7bf3b5097cf63be2539c2e694c168bd824ba468ca87cb17be801b72b972ab417da98d1b5473f319afd642bf5c6c0270e3a697d016

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-py
BuildRequires:  python-xml
BuildRequires:  python-hypothesis
BuildRequires:  python-Twisted
BuildRequires:  python-setuptools_scm

BuildRequires:  python3-devel
BuildRequires:  python3-py
BuildRequires:  python3-hypothesis
BuildRequires:  python3-Twisted
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools_scm

Requires:       python2
Requires:       python-py

BuildArch:      noarch

%description
pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.

%package -n     python3-pytest
Summary:        pytest is a mature full-featured Python testing tool that helps you write better programs
Requires:       python3
Requires:       python3-py
# need to install importlib-metadata more-itertools
# using pip after installation
Requires:       python3-atomicwrites
Requires:       python3-attrs
Requires:       python3-setuptools
Requires:       python3-packaging

%description -n python3-pytest

Python 3 version.

%prep
%autosetup -p1 -n pytest-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
%py_build
pushd ../p3dir
%py3_build
popd

%install
%py_install

mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest%{python_version}
ln -snf pytest%{python2_version} %{buildroot}%{_bindir}/pytest2
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test%{python_version}
ln -snf py.test%{python2_version} %{buildroot}%{_bindir}/py.test2

pushd ../p3dir
%py3_install
mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest%{python3_version}
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest3
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest-%{python3_version}
mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test%{python3_version}
ln -snf py.test%{python3_version} %{buildroot}%{_bindir}/py.test3
popd

%check
make -k check %{?_smp_mflags}

%files
%defattr(-,root,root,-)
%{_bindir}/pytest2
%{_bindir}/py.test2
%{_bindir}/pytest%{python_version}
%{_bindir}/py.test%{python_version}
%{python_sitelib}/*

%files -n python3-pytest
%defattr(-,root,root,-)
%{_bindir}/pytest-%{python3_version}
%{_bindir}/pytest3
%{_bindir}/pytest
%{_bindir}/py.test3
%{_bindir}/pytest%{python3_version}
%{_bindir}/py.test%{python3_version}
%{python3_sitelib}/*

%changelog
* Mon Oct 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.8.2-2
- Fix python3-pytest requires
- Fix packaging
* Tue Oct 09 2018 Tapas Kundu <tkundu@vmware.com> 3.8.2-1
- Updated to release 3.8.2
- Removed buildrequires from subpackage.
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.7-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0.7-2
- Use python2 instead of python and rename the scripts in bin directory
* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0.7-1
- Initial
