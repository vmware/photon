%define srcname mistune

Summary:        The fastest markdown parser in pure Python.
Name:           python3-mistune
Version:        2.0.5
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/mistune

Source0: https://files.pythonhosted.org/packages/source/m/mistune/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=109447977a441ebbedfca2abbe62415139d94c48ae56c3d8cae04df3f93ccd1e8333b3dbb8bf61a2096b903df6c3aab2fadd0893fb82815416f17555465e98c7

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-pip
%endif

Requires: python3

BuildArch: noarch

%description
The fastest markdown parser in pure Python with renderer features, inspired by marked.

%prep
%autosetup -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%check
pip3 install tomli
%{pytest}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.0.5-2
- Release bump for SRP compliance
* Sun Aug 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.5-1
- Upgrade to v2.0.5
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.4-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.4-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.4-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.8.3-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.8.3-1
- Update to version 0.8.3
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.4-1
- Initial packaging for Photon
