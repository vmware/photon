%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-typing
Version:        3.6.6
Release:        2%{?dist}
Summary:        Type Hints for Python
License:        PSF
Group:          Development/Tools
Url:            https://docs.python.org/3/library/typing.html
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/17/75/3698d7992a828ad6d7be99c0a888b75ed173a9280e53dbae67326029b60e/typing-%{version}.tar.gz
%define sha1    typing=8414f7e523f1f286f72392e9f8929d346df6f6a2

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Typing defines a standard notation for Python function and variable type annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime type checkers, static analyzers, IDEs and other tools.

%prep
%setup -q -n typing-%{version}

%build
python3 setup.py build

%install
rm -rf %{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python3 python3/test_typing.py


%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 3.6.6-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.6.6-1
-   Update to version 3.6.6
*   Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.6.1-3
-   Adding python3 version.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-2
-   Use python2 explicitly
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-1
-   Initial
