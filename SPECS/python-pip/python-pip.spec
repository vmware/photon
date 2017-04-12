Name:           python-pip
Version:        9.0.1
Release:        2%{?dist}
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

%description
The PyPA recommended tool for installing Python packages.


%prep
%setup -q -n pip-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install freezegun
%{__python} setup.py test

%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/*

%changelog
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-2
-   Added python-setuptools to requires.
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 9.0.1-1
-   Upgrade version to 9.0.1
*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-1
-   Initial packaging for Photon
