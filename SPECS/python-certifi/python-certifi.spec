%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-certifi
Version:        2018.8.24
Release:        1%{?dist}
Summary:        Python package for providing Mozilla's CA Bundle
License:        MPL-2.0
URL:            https://github.com/certifi
Source0:        https://pypi.org/project/certifi/certifi-%{version}.tar.gz
%define sha1    certifi=cc1ab6c25a8c8079ab3ff1019530506cfd59bef7
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  ca-certificates
Requires:       ca-certificates

%description
Certifi is a carefully curated collection of
Root Certificates for validating the trustworthiness of 
SSL certificates while verifying the identity of TLS hosts

%package -n python2-certifi
Summary: Character encoding auto-detection in Python
%description -n python2-certifi
Python 2 version

%package -n python3-certifi
Summary: Character encoding auto-detection in Python 3
%description -n python3-certifi
Python 3 version.

%prep
%setup -n certifi-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
python3 setup.py test

%files -n python2-certifi
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-certifi
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 18.3-1
-   Upgraded version to 18.3

