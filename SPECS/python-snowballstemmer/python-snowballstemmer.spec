%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-snowballstemmer
Version:        1.2.1
Release:        3%{?dist}
Summary:        Python stemming library
License:        BSD
Group:          Development/Languages/Python
Url:            https://github.com/shibukawa/snowball_py
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/20/6b/d2a7cb176d4d664d94a6debf52cd8dbae1f7203c8e42426daa077051d59c/snowballstemmer-%{version}.tar.gz
%define sha1    snowballstemmer=377be08ed935d401a53cba79319d1812cfe46b81

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

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


%prep
%setup -n snowballstemmer-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.2.1-3
-   Mass removal python2
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-2
-   Use python2 explicitly
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-1
-   Initial
