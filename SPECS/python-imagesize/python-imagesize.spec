Name:           python3-imagesize
Version:        1.4.1
Release:        2%{?dist}
Summary:        python module to analyze jpeg/jpeg2000/png/gif image header and return image size.
Group:          Development/Languages/Python
Url:            https://github.com/shibukawa/imagesize_py
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: https://github.com/shibukawa/imagesize_py/archive/refs/tags/imagesize-%{version}.tar.gz
%define sha512  imagesize=f191d7fe34a01ab21b0f4f6519df8ab2a53c1ca54956f4d825d9cec5bd5f4c569491bdc26cb36fcaad2c453c35e51f69379f091362e206453aaefbda4802daa4

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-packaging

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

%description
python module to analyze jpeg/jpeg2000/png/gif image header and return image size.

%prep
%autosetup -p1 -n imagesize-%{version}

%build
%py3_build

%install
%py3_install

%check
py.test3

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.1-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.4.1-1
- Automatic Version Bump
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-2
- Fix build with new rpm
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.0-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 1.1.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.1.0-1
- Update to version 1.1.0
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.1-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.1-2
- Change python to python2
* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.1-1
- Initial Build
