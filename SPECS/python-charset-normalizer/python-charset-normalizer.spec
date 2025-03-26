Name:           python3-charset-normalizer
Version:        2.1.1
Release:        2%{?dist}
Summary:        The Real First Universal Charset Detector
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/ousret/charset_normalizer

Source0: charset-normalizer-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.1.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.1-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0.9-1
- Initial verision, needed for python3-requests-2.26.0
