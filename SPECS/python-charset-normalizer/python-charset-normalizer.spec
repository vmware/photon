Name:           python3-charset-normalizer
Version:        2.1.1
Release:        1%{?dist}
Summary:        The Real First Universal Charset Detector
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://github.com/ousret/charset_normalizer

Source0: charset-normalizer-%{version}.tar.gz
%define sha512 charset-normalizer=f52abab683ebda4100d67ec6ee0349713baee453a742d60a1356f405c5ce2c3b4d850b0891527f08f92fa1217d59c46d6b181dc4ff1b962ce60d9c5ef8c913d1

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-setuptools

BuildArch:      noarch

%description
A library that helps you read text from an unknown charset encoding.
Motivated by chardet, trying to resolve the issue by taking
a new approach. All IANA character set names for which the Python core
library provides codecs are supported.

%prep
%autosetup -p1 -n charset-normalizer-%{version}
# Remove pytest-cov settings from setup.cfg
sed -i "/addopts = --cov/d" setup.cfg

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
%pytest
%endif

%files
%defattr(-,root,root)
%{_bindir}/normalizer
%{python3_sitelib}/*

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.1-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0.9-1
- Initial verision, needed for python3-requests-2.26.0
