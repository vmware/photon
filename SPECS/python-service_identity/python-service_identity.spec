Summary:        Service identity verification for pyOpenSSL.
Name:           python3-service_identity
Version:        21.1.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/service_identity

Source0:        service_identity-%{version}.tar.gz
%define sha512  service_identity=36a6f7cb30871bd38da865521503c622a70318f8c5cdc74b0565bdc292bb3b84682bf3afe050d007b21f27d0c54ba0bfe1cd71b63fb13fa42cbaef66cb115c2b

BuildRequires:  python3-devel
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
Requires:       python3-pyasn1-modules
Requires:       python3-pyasn1
Requires:       python3-attrs
Requires:       python3-pyOpenSSL

BuildArch:      noarch

%description
service_identity aspires to give you all the tools you need for verifying whether a certificate is valid for the intended purposes.

In the simplest case, this means host name verification. However, service_identity implements RFC 6125 fully and plans to add other relevant RFCs too.

%prep
%autosetup -n service-identity-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pathlib2 funcsigs pluggy atomicwrites more-itertools
PYTHONPATH="%{buildroot}%{python3_sitelib}" py.test3

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 21.1.0-2
- Bump version as a part of python3-pyOpenSSL upgrade
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 21.1.0-1
- Automatic Version Bump
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
