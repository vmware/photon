%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-enum
Version:        0.4.7
Release:        2%{?dist}
Summary:        Robust enumerated type support in Python
License:        GNU General Public License (GPL) (GPL-3.0+)
Group:          Development/Languages/Python
Url:            http://pypi.python.org/packages/source/e/enum/enum-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:        enum-%{version}.tar.gz
%define sha1    enum=dccaa3ebd20ecba27192b6fb2462a197e1df7864

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
This package provides a module for robust enumerations in Python. 

%prep
%setup -n enum-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%changelog
*   Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 0.4.7-2
-   Updated the license.
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.4.7-1
-   Update to version 0.4.7
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.4.6-2
-   Changed python to python2
*   Thu Feb 16 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.6-1
-   Initial packaging for Photon
