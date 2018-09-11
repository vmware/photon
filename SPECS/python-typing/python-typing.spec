%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-typing
Version:        3.6.6
Release:        1%{?dist}
Summary:        Type Hints for Python
License:        PSF
Group:          Development/Tools
Url:            https://docs.python.org/3/library/typing.html
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/17/75/3698d7992a828ad6d7be99c0a888b75ed173a9280e53dbae67326029b60e/typing-%{version}.tar.gz
%define sha1    typing=8414f7e523f1f286f72392e9f8929d346df6f6a2

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

%package -n     python3-typing
Summary:        python3 version
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-typing
Python 3 version.

%prep
%setup -q -n typing-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
rm -rf %{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%clean
rm -rf %{buildroot}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python2_sitelib} \
    python2 python2/test_typing.py


%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-typing
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.6.6-1
-   Update to version 3.6.6
*   Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.6.1-3
-   Adding python3 version.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-2
-   Use python2 explicitly
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-1
-   Initial
