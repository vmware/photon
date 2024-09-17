%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python package for providing Mozilla's CA Bundle
Name:           python-certifi
Version:        2023.11.17
Release:        2%{?dist}
URL:            https://github.com/certifi
License:        MPL-2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/certifi/python-certifi/archive/certifi-%{version}.tar.gz
%define sha512  certifi=873eb3a34c5061f164484eec5bc659d4869882c96477395eec7d9d52242a033f9d82d293b07bcb094d04e62dc9af8a65caf2385a1a2a78c7058252af1b3d715b
Patch0:         CVE-2024-39689.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  ca-certificates
%if 0%{?with_check}
BuildRequires:  python-pytest
BuildRequires:  python3-pytest
%endif

Requires:       ca-certificates

BuildArch:      noarch

%description
Certifi is a carefully curated collection of
Root Certificates for validating the trustworthiness of
SSL certificates while verifying the identity of TLS hosts

%package -n     python3-certifi
Summary:        Python 3 certifi library

Requires:       ca-certificates

%description -n python3-certifi
Python 3 version of certifi.

%prep
%autosetup -p1

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
* Tue Sep 17 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2023.11.17-2
- Fix CVE-2024-39689
* Tue Dec 19 2023 Prashant S Chauhan <psinghchauha@vmware.com> 2023.11.17-1
- Update to 2023.11.17, Fixes CVE-2023-37920
* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 2018.08.24-1
- Initial packaging
