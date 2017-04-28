%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-alabaster
Version:        0.7.10
Release:        1%{?dist}
Summary:        A configurable sidebar-enabled Sphinx theme
License:        BSD
Group:          Development/Languages/Python
Url:            https://github.com/bitprophet/alabaster/
Source0:        https://pypi.python.org/packages/d0/a5/e3a9ad3ee86aceeff71908ae562580643b955ea1b1d4f08ed6f7e8396bd7/alabaster-%{version}.tar.gz
%define sha1    alabaster=dba599faf1ca5541ef35ab251eb2b365ae2f25c7

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Alabaster is a visually (c)lean, responsive, configurable theme for the Sphinx documentation system. It is Python 2+3 compatible.

%package -n     python3-alabaster
Summary:        A configurable sidebar-enabled Sphinx theme
BuildRequires:  python3
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-libs

%description -n python3-alabaster

Python 3 version.

%prep
%setup -n alabaster-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%files -n python3-alabaster
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.10-1
-   Initial
