Name:           python3-snowballstemmer
Version:        2.2.0
Release:        2%{?dist}
Summary:        Python stemming library
Group:          Development/Languages/Python
Url:            https://github.com/shibukawa/snowball_py
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: https://pypi.python.org/packages/20/6b/d2a7cb176d4d664d94a6debf52cd8dbae1f7203c8e42426daa077051d59c/snowballstemmer-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description
This package provides 16 stemmer algorithms (15 + Poerter English stemmer) generated from Snowball algorithms.
It includes following language algorithms:

* Danish
* Dutch
* English (Standard, Porter)
* Finnish
* French
* German
* Hungarian
* Italian
* Norwegian
* Portuguese
* Romanian
* Russian
* Spanish
* Swedish
* Turkish

%prep
%autosetup -p1 -n snowballstemmer-%{version}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 1.2.1-3
- Mass removal python2
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-2
- Use python2 explicitly
* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-1
- Initial
