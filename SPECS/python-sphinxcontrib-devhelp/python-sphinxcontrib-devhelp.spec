%define srcname sphinxcontrib-devhelp

Name:           python3-sphinxcontrib-devhelp
Version:        1.0.2
Release:        4%{?dist}
Summary:        Sphinx extension for Devhelp documents
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
URL:            https://pypi.org/project/sphinxcontrib-devhelp
Distribution:   Photon

BuildArch: noarch

Source0: https://files.pythonhosted.org/packages/98/33/dc28393f16385f722c893cb55539c641c9aaec8d1bc1c15b69ce0ac2dbb3/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=83b46eaf26df3932ea2136cfda1c0fca4fc08ce8bca564845b3efe5bb00d6c8c93991f4edd4913d4ec796e2d85bd2c7265adf28e98f42e8094daeb5ac11a0eb1

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3
Requires: python3-docutils

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-devhelp is a sphinx extension which outputs Devhelp document.

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.0.2-4
- Release bump for SRP compliance
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-3
- Add python3-docutils to requires
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-2
- Update release to compile with python 3.11
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-1
- initial version
