%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-snowballstemmer
Version:        1.2.1
Release:        1%{?dist}
Summary:        Python stemming library
License:        BSD
Group:          Development/Languages/Python
Url:            https://github.com/shibukawa/snowball_py
Source0:        https://pypi.python.org/packages/20/6b/d2a7cb176d4d664d94a6debf52cd8dbae1f7203c8e42426daa077051d59c/snowballstemmer-%{version}.tar.gz
%define sha1    snowballstemmer=377be08ed935d401a53cba79319d1812cfe46b81

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
This package provides 16 stemmer algorithms (15 + Poerter English stemmer) generated from Snowball algorithms. 
It includes following language algorithms:

* Danish
* Dutch
* English (Standard, Porter)
* Finnish
* French
* German
* Hungarian
* Italian
* Norwegian
* Portuguese
* Romanian
* Russian
* Spanish
* Swedish
* Turkish

%package -n     python3-snowballstemmer
Summary:        Python stemming library
BuildRequires:  python3
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-libs

%description -n python3-snowballstemmer

Python 3 version.

%prep
%setup -n snowballstemmer-%{version}
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

%files -n python3-snowballstemmer
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-1
-   Initial
