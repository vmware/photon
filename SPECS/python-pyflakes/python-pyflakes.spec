%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-pyflakes
Version:        2.3.1
Release:        1%{?dist}
Summary:        A simple program which checks Python source files for errors
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/PyCQA/pyflakes/archive/refs/tags/%{version}.tar.gz
Source0:        pyflakes-%{version}.tar.gz
%define sha1    pyflakes=9798bb913a46fc8352d75098d94c837ec3559393
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

%description
Pyflakes is similar to PyChecker in scope, but differs in that it does
not execute the modules to check them. This is both safer and faster,
although it does not perform as many checks. Unlike PyLint, Pyflakes
checks only for logical errors in programs; it does not perform any
check on style.

%prep
%autosetup -n pyflakes-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{_bindir}/pyflakes
%{python3_sitelib}/*

%changelog
*   Fri Jul 09 2021 Tapas Kundu <tkundu@vmware.com> 2.3.1-1
-   Initial packaging for python3-pyflakes
