Name:           python3-py
Version:        1.11.0
Release:        3%{?dist}
Summary:        Python development support library
Group:          Development/Languages/Python
Url:            https://github.com/pytest-dev/py
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pytest-dev/py/archive/refs/tags/py-%{version}.tar.gz
%define sha512 py=ce8dd791f9f6dd7e60a6caad32ff5cb816389a0840436efdedf4e0d4b0bfa09f7aea9e7c31d89903c72fe6ef17170a85af480525ba92c458ed73501a0420f2c4

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml
BuildRequires:  python3-wheel
BuildRequires:  python3-typing-extensions

%if 0%{?with_check}
BuildRequires: python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

%description
The py lib is a Python development support library featuring the following tools and modules:

py.path: uniform local and svn path objects
py.apipkg: explicit API control and lazy-importing
py.iniconfig: easy parsing of .ini files
py.code: dynamic code generation and introspection

%prep
%autosetup -p1 -n py-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
%pytest
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.11.0-3
- Release bump for SRP compliance
* Fri Jul 19 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 1.11.0-2
- Use system provided packages to do offline build
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.11.0-1
- Automatic Version Bump
* Mon Jun 21 2021 Dweep Advani <dadvani@vmware.com> 1.9.0-2
- Patched for CVE-2020-29651
* Tue Jul 28 2020 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
- Updated to version 1.9.0
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 1.6.0-2
- Mass removal python2
* Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 1.6.0-1
- Updated to versiob 1.6.0
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.4.33-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.33-2
- Use python2_sitelib
* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.33-1
- Initial Build
