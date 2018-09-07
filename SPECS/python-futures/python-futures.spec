%define sha1    futures=e6815bea6a2881218df730347732f67ec5e89108
Name:           python-futures
Version:        3.2.0
Release:        1%{?dist}
Summary:        Backport of the concurrent.futures package to Python 2.6 and 2.7
License:        PSF
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/futures
Source0:        https://pypi.python.org/packages/cc/26/b61e3a4eb50653e8a7339d84eeaa46d1e93b92951978873c220ae64d0733/futures-%{version}.tar.gz
%define sha1    futures=e6815bea6a2881218df730347732f67ec5e89108
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  pkg-config
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
BuildArch:	noarch
%description
Backport of the concurrent.futures package to Python 2.6 and 2.7

%prep
%setup -n futures-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Fri Sep 07 2018 Tapas Kundu <tkundu@vmware.com> 3.2.0-1
-   Update to version 3.2.0
*   Thu Apr 06 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.1-1
-   Initial version of python-fuse package for Photon.
