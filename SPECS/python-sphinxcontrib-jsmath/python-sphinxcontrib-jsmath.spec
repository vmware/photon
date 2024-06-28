%define srcname sphinxcontrib-jsmath

Name:           python3-sphinxcontrib-jsmath
Version:        1.0.1
Release:        3%{?dist}
Summary:        Sphinx extension for math in HTML via JavaScript
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-jsmath
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/b2/e8/9ed3830aeed71f17c026a07a5097edcf44b692850ef215b161b8ad875729/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=c1e6488f5c0ca4567c27ec7c597c9db321ac32ce354c4ad62fea534b2ae1c0acb183a921f46216bbc3891f14acfaac05ddf324b8fdaf99828df07bc91aa7e5c7

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-jsmath is a sphinx extension which renders display math in HTML
via JavaScript.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.rst
%{python3_sitelib}/*

%changelog
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-3
- Fix summary & description
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.1-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-1
- initial version
