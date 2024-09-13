Summary:        Service identity verification for pyOpenSSL.
Name:           python3-service_identity
Version:        18.1.0
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/service_identity
Source0:        service_identity-%{version}.tar.gz
%define sha512  service_identity=c1556e385035a8d43fd0e3960c0396b9d2536c5e3c7450b3669c8c9b8ff60b6a9d2f0282dc30c1fb46034b4abcb0ff6d74ed79f6bcc33f59035988ccaf3324d2
Source1:        service_identity_tests-%{version}.tar.gz
%define sha512  service_identity_tests=35317088a38ff9654abac84603ab85fa91eeb7a52f3870bde82e4cca94ed3a9b4041f9af7475795f67d2c0b13a85a5122f842e53929b61f60f1c9e866566a495
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-pyasn1-modules
BuildRequires:  python3-pyasn1
BuildRequires:  python3-attrs
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-idna
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-pyasn1-modules
Requires:       python3-pyasn1
Requires:       python3-attrs
Requires:       python3-pyOpenSSL

BuildArch:      noarch

%description
service_identity aspires to give you all the tools you need for verifying whether a certificate is valid for the intended purposes.
In the simplest case, this means host name verification. However, service_identity implements RFC 6125 fully and plans to add other relevant RFCs too.

%prep
%autosetup -p1 -n service_identity-%{version}
tar xf %{SOURCE1} --no-same-owner

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip3 install pathlib2
pip3 install funcsigs
pip3 install pluggy
pip3 install atomicwrites
pip3 install more-itertools
PYTHONPATH="%{buildroot}%{python3_sitelib}" py.test3

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Fri Sep 13 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 18.1.0-5
- Bump-up to compile with python3-attrs-22.2.0
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 18.1.0-4
- Bump up to compile with python 3.10
* Tue Nov 30 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 18.1.0-3
- Increment for openssl 3.0.0 compatibility
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 18.1.0-2
- Mass removal python2
* Mon Jun 01 2020 Tapas Kundu <tkundu@vmware.com> 18.1.0-1
- Update to 18.1.0
* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 17.0.0-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.0.0-1
- Update to version 17.0.0
* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 16.0.0-3
- Fixed runtime dependencies
- Fixed make check errors
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.0.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 16.0.0-1
- Initial packaging for Photon.
