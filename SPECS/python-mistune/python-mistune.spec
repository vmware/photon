%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The fastest markdown parser in pure Python.
Name:           python3-mistune
Version:        0.8.4
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/mistune/
Source0:        https://files.pythonhosted.org/packages/source/m/mistune/mistune-%{version}.tar.gz
%define sha1    mistune=fd210c038fa7b0f2dffad6847b17dc139e7dd9fe

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
The fastest markdown parser in pure Python

The fastest markdown parser in pure Python with renderer features, inspired by marked.


%prep
%setup -q -n mistune-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.4-1
-   Automatic Version Bump
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.8.3-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.8.3-1
-   Update to version 0.8.3
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-1
-   Initial packaging for Photon
