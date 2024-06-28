%define srcname requests-unixsocket

Name:           python3-requests-unixsocket
Version:        0.3.0
Release:        1%{?dist}
Summary:        Use requests to talk HTTP via a UNIX domain socket
License:        Apache-2
Url:            https://pypi.org/project/requests-unixsocket
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/c3/ea/0fb87f844d8a35ff0dcc8b941e1a9ffc9eb46588ac9e4267b9d9804354eb/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=21c887b0c3fa526a2debb3960e0ea4dc3b3015cdd517459b6484501176321408d1b4c87dd2840c7d8b71d08fa9114f655ae03f8bc9ff1fca33c914900ef82f5b

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-requests
BuildRequires: python3-pip

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: python3

BuildArch: noarch

%description
Requests is an Apache2 Licensed HTTP library, written in Python, for human
beings.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
pip3 install pep8 pytest-cache pytest-pep8 waitress
python3 -m pytest -v
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Thu Aug 11 2022 Tapas Kundu <tkundu@vmware.com> 0.3.0-1
- Initial addition
