%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-netifaces
Version:        0.10.9
Release:        2%{?dist}
Summary:        Python library to retrieve information about network interfaces
Group:          Development/Libraries
License:        MIT
URL:            http://alastairs-place.net/netifaces/
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/n/netifaces/netifaces-%{version}.tar.gz
%define sha1    netifaces=340a91e6cdd03c941a0da464255d6e4b5cbe5512
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description
This package provides a cross platform API for getting address information
from network interfaces.


%prep
%setup -q -n netifaces-%{version}

%build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%doc README.rst
%{python3_sitelib}/*

%changelog
*  Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.10.9-2
-  Mass removal python2
*  Tue Jul 23 2019 Tapas Kundu <tkundu@vmware.com> 0.10.9-1
-  Initial packaging for photon OS
