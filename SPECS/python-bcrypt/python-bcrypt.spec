%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-bcrypt
Version:        3.1.6
Release:        3%{?dist}
Summary:        Good password hashing for your software and your servers.
License:        Apache License, Version 2.0
Group:          Development/Languages/Python
Url:            http://pypi.python.org/packages/source/e/bcrypt/bcrypt-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        bcrypt-%{version}.tar.gz
%define sha1    bcrypt=03a17719edea2f3d1e32b5c510171df304769542

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
%if %{with_check}
BuildRequires:  curl-devel
%endif

%description
Good password hashing for your software and your servers.


%prep
%setup -n bcrypt-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 3.1.6-3
-   Mass removal python2
*   Tue Sep 03 2019 Shreyas B. <shreyasb@vmware.com> 3.1.6-2
-   Fix make check errors.
*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 3.1.6-1
-   Initial packaging for Photon
