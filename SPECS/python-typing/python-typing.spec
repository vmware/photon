%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-typing
Version:        3.6.1
Release:        1%{?dist}
Summary:        Type Hints for Python
License:        PSF
Group:          Development/Tools
Url:            https://docs.python.org/3/library/typing.html
Source0:        https://pypi.python.org/packages/17/75/3698d7992a828ad6d7be99c0a888b75ed173a9280e53dbae67326029b60e/typing-%{version}.tar.gz
%define sha1    typing=d6ce2f6379d2594c174adb1c94643297600c979c

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Typing defines a standard notation for Python function and variable type annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime type checkers, static analyzers, IDEs and other tools.

%prep
%setup -n typing-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python_sitelib} \
    python2 python2/test_typing.py

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-1
-   Initial
