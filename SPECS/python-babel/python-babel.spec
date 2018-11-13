%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-babel
Version:        2.6.0
Release:        2%{?dist}
Summary:        an integrated collection of utilities that assist in internationalizing and localizing Python applications
License:        BSD3
Group:          Development/Languages/Python
Url:            http://babel.pocoo.org
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/92/22/643f3b75f75e0220c5ef9f5b72b619ccffe9266170143a4821d4885198de/Babel-%{version}.tar.gz
%define sha1    Babel=6aed99e4fb8a2a75de7815599f610cdcbb81e3c2

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytz
BuildRequires:  python-pytest
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-pytz
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python-six
BuildRequires:  python3-six
BuildRequires:  python-attrs
BuildRequires:  python3-attrs
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-pytz
BuildArch:      noarch

%description
Babel is an integrated collection of utilities that assist in internationalizing and localizing Python applications,
with an emphasis on web-based applications.

The functionality Babel provides for internationalization (I18n) and localization (L10N) can be separated into two different aspects:
1.Tools to build and work with gettext message catalogs.
2.A Python interface to the CLDR (Common Locale Data Repository), providing access to various locale display names, localized number and date formatting, etc.

%package -n     python3-babel
Summary:        an integrated collection of utilities that assist in internationalizing and localizing Python applications
Requires:       python3
Requires:       python3-libs
Requires:       python3-pytz

%description -n python3-babel

Python 3 version.

%prep
%setup -n Babel-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/pybabel %{buildroot}/%{_bindir}/pybabel3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pytest freezegun funcsigs pathlib2 pluggy utils
python2 setup.py test
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest freezegun funcsigs pathlib2 pluggy utils
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%{_bindir}/pybabel
%{python2_sitelib}/*

%files -n python3-babel
%defattr(-,root,root,-)
%{_bindir}/pybabel3
%{python3_sitelib}/*

%changelog
*   Tue Nov 13 2018 Tapas Kundu <tkundu@vmware.com> 2.6.0-2
-   Fixed make check errors.
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.6.0-1
-   Update to version 2.6.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.0-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.0-2
-   Change python to python2 and add python2 scripts to bin directory
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.0-1
-   Initial
