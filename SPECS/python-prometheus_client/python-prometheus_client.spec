%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-prometheus_client
Version:        0.8.0
Release:        1%{?dist}
Summary:        Python client for the Prometheus monitoring system.
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/prometheus_client
Source0:        prometheus_client-%{version}.tar.gz
%define sha1    prometheus_client=5846c9dfad32c2bc335bbeac1011a900e686e974
Source1:        client_python-tests-%{version}.tar.gz
%define sha1    client_python-tests=3f3be721edfd2ae04d32bbab48d416b9042b8684
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools

BuildArch:      noarch

%description
Python client for the Prometheus monitoring system.


%prep
%setup -n prometheus_client-%{version}
tar xf %{SOURCE1} --no-same-owner

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
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.0-1
-   Automatic Version Bump
*   Tue Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 0.3.1-3
-   Mass removal python2
*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 0.3.1-2
-   Fix make check
-   uploaded test source
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.3.1-1
-   Update to version 0.3.1
*   Tue Sep 19 2017 Bo Gan <ganb@vmware.com> 0.0.20-2
-   fix make check issue by using upstream sources
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.0.20-1
-   Initial version of python-prometheus_client package for Photon.
