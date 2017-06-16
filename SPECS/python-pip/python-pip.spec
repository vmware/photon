%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           python-pip
Version:        9.0.1
Release:        5%{?dist}
Url:            https://pypi.python.org/pypi/pip
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-%{version}.tar.gz 
%define sha1 pip=57ff41e99cb01b6a1c2b0999161589b726f0ec8b
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
Requires:       python-xml

BuildArch:      noarch

%description
The PyPA recommended tool for installing Python packages.


%prep
%setup -q -n pip-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install freezegun
python2 setup.py test

%files
%defattr(-,root,root)
%{python2_sitelib}/*
%{_bindir}/*

%changelog
*   Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.0.1-5
-   Use python2 explicitly
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-4
-   Add python-xml to requires.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.0.1-3
-   Fix arch
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-2
-   Added python-setuptools to requires.
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 9.0.1-1
-   Upgrade version to 9.0.1
*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-1
-   Initial packaging for Photon
