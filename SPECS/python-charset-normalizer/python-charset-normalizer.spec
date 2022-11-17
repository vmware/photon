Name:           python3-charset-normalizer
Version:        2.0.9
Release:        1%{?dist}
Summary:        The Real First Universal Charset Detector
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://github.com/ousret/charset_normalizer

Source0: charset-normalizer-%{version}.tar.gz
%define sha512 charset-normalizer=0dea4ada59c197a1f7090b0c06218774746f77c2007eaff37dae4589cab1382ed670c98327d890347d2b72869b6053eb8c3362587b034921958624b9db9aff95

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
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0.9-1
- Initial verision, needed for python3-requests-2.26.0
