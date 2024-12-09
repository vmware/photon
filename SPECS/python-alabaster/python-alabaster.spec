Name:           python3-alabaster
Version:        0.7.12
Release:        3%{?dist}
Summary:        A configurable sidebar-enabled Sphinx theme
Group:          Development/Languages/Python
Url:            https://github.com/bitprophet/alabaster
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://pypi.python.org/packages/d0/a5/e3a9ad3ee86aceeff71908ae562580643b955ea1b1d4f08ed6f7e8396bd7/alabaster-%{version}.tar.gz
%define sha512 alabaster=e3bfd0c92ce01f08d5e6d9dc1ef0967ca1f54827e08756f4a0ba7be8d3b8bec7f2e53a169b831ff5ce2d2548f7f52c6e518bcc513e49bb3e4c38274293aebbac

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
BuildArch:      noarch

%description
Alabaster is a visually (c)lean, responsive, configurable theme for the Sphinx documentation system. It is Python 2+3 compatible.

%prep
%autosetup -p1 -n alabaster-%{version}

%build
%py3_build

%install
%py3_install

%check
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.7.12-3
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.7.12-2
- Update release to compile with python 3.11
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.7.12-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.7.11-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.7.11-1
- Update to version 0.7.11
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.10-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.10-2
- Changed python to python2
* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.10-1
- Initial
