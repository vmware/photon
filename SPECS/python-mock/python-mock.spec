%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-mock
Version:        4.0.3
Release:        1%{?dist}
Summary:        Rolling backport of unittest.mock for all Pythons
License:        BSD License
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/e2/be/3ea39a8fd4ed3f9a25aae18a1bff2df7a610bca93c8ede7475e32d8b73a0/mock-4.0.3.tar.gz
Source0:        mock-%{version}.tar.gz
%define sha1    mock=348e1bd2d19bd25819709ec1adc0b04c926c9a0c
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch
Provides:       python3.9dist(mock)

%description
mock is a library for testing in Python. It allows you to replace parts of your system under test with mock objects and make assertions about how they have been used.
mock is now part of the Python standard library, available as unittest.mock in Python 3.3 onwards.
This package contains a rolling backport of the standard library mock code compatible with Python 3.6 and up.

%prep
%autosetup -n mock-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 4.0.3-1
-   Initial packaging for python3-mock
