Name:           python3-vcversioner
Version:        2.16.0.0
Release:        4%{?dist}
Summary:        Python version extractor
Group:          Development/Languages/Python
Url:            https://github.com/habnabit/vcversioner
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: vcversioner-%{version}.tar.gz
%define sha512 vcversioner=e4e34693aa813e57991eca01d20102bd2e939b536461e2e9e063ac0e3558580e57d7e8d5e08d010690b3c901c97e53f187f20b48520b333eb492ec33e85757d8

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xml

BuildArch:      noarch

%description
Elevator pitch: you can write a setup.py with no version information specified, and vcversioner will find a recent, properly-formatted VCS tag and extract a version from it.

%prep
%autosetup -p1 -n vcversioner-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.16.0.0-4
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.16.0.0-3
- Update release to compile with python 3.11
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 2.16.0.0-2
- Mass removal python2
* Tue Oct 23 2018 Sujay G <gsujay@vmware.com> 2.16.0.0-1
- Initial version
