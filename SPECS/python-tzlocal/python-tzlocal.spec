%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        tzinfo object for the local timezone.
Name:           python-tzlocal
Version:        1.5.1
Release:        1%{?dist}
License:        MIT License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/tzlocal/1.4
Source0:        https://files.pythonhosted.org/packages/source/t/tzlocal/tzlocal-%{version}.tar.gz
%define sha1    tzlocal=98dc51724f3201f66f4ec36f22b99bd03f3059bd
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six

Requires:       python2
Requires:       python2-libs
Requires:       python-pytz
BuildArch:      noarch

%description
This Python module returns a tzinfo object with the local timezone information under Unix and Win-32. It requires pytz, and returns pytz tzinfo objects.

This module attempts to fix a glaring hole in pytz, that there is no way to get the local timezone information, unless you know the zoneinfo name, and under several Linux distros that’s hard or impossible to figure out.

Also, with Windows different timezone system using pytz isn’t of much use unless you separately configure the zoneinfo timezone name.

With tzlocal you only need to call get_localzone() and you will get a tzinfo object with the local time zone info. On some Unices you will still not get to know what the timezone name is, but you don’t need that when you have the tzinfo file. However, if the timezone name is readily available it will be used.

%package -n     python3-tzlocal
Summary:        python-tzlocal
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-six
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs
Requires:       python3-pytz

%description -n python3-tzlocal
Python 3 version.

%prep
%setup -q -n tzlocal-%{version}
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
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-tzlocal
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.5.1-1
-   Update to version 1.5.1
*   Mon Sep 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.4-1
-   Initial packaging for Photon
