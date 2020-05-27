%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python package for providing Mozilla's CA Bundle
Name:           python-certifi
Version:        2018.08.24
Release:        1%{?dist}
URL:            https://github.com/certifi
License:        MPL-2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/certifi/python-certifi/archive/certifi-%{version}.tar.gz
%define sha1    certifi=7433702a8c690e6cf6e7108e7bd3d8999d4976d6

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  ca-certificates
%if %{with_check}
BuildRequires:  python-pytest
%endif

Requires:       ca-certificates

BuildArch:      noarch

%description
Certifi is a carefully curated collection of
Root Certificates for validating the trustworthiness of
SSL certificates while verifying the identity of TLS hosts

%package -n     python3-certifi
Summary:        Python 3 certifi library

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pytest
%endif

Requires:       ca-certificates

%description -n python3-certifi
Python 3 version of certifi.

%prep
%setup -q -n python-certifi-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-certifi
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 2018.08.24-1
-   Initial packaging
