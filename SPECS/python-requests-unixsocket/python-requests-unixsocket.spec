%define srcname requests-unixsocket

Name:           python3-requests-unixsocket
Version:        0.3.0
Release:        4%{?dist}
Summary:        Use requests to talk HTTP via a UNIX domain socket
Url:            https://pypi.org/project/requests-unixsocket
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/c3/ea/0fb87f844d8a35ff0dcc8b941e1a9ffc9eb46588ac9e4267b9d9804354eb/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: fix-for-requests.patch

BuildRequires: python3-devel
BuildRequires: python3-pbr
BuildRequires: python3-setuptools
BuildRequires: python3-requests
BuildRequires: python3-pip

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires: python3
Requires: python3-requests >= 2.28.1-7

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
* Tue Jan 28 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-4
- Fix functionality break introduced by CVE-2024-35195 in python3-requests
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-3
- Release bump for SRP compliance
* Mon Jun 03 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.3.0-2
- Use system provided packages to do offline build
* Thu Aug 11 2022 Tapas Kundu <tkundu@vmware.com> 0.3.0-1
- Initial addition
