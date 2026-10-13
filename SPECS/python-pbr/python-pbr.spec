%global build_if %{photon_subrelease} >= 92

Summary:        Python Build Reasonableness
Name:           python3-pbr
Version:        7.1.3
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://docs.openstack.org/developer/pbr/
Source0: https://github.com/openstack/pbr/archive/refs/tags/%{version}.tar.gz#/pbr-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-docutils
BuildRequires:  python3-setuptools
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-packaging
BuildRequires:  python3-devel
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  git
BuildRequires:  python3-pip
BuildRequires:  python3-virtualenv
BuildRequires:  python3-wheel
%endif

Requires:       python3

BuildArch:      noarch
%description
A library for managing setuptools packaging needs in a consistent manner.

%prep
%autosetup -n pbr-%{version}

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%py3_build_wheel

%install
export PBR_VERSION=%{version}
%py3_install_wheel
%{py_byte_compile_and_ghost}
mv %{buildroot}/%{_bindir}/pbr %{buildroot}/%{_bindir}/pbr3

%if 0%{?with_check}
%check
pip3 install testtools fixtures testscenarios testresources
# the functional tests need network access to install packages
rm -rf pbr/tests/functional
PBR_VERSION=%{version} python3 -m testtools.run discover -s pbr/tests -t .
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_bindir}/pbr3
%{python3_sitelib}/pbr-%{version}.dist-info
%{python3_sitelib}/pbr

%changelog
* Tue Oct 13 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.1.3-1
- Upgrade to 7.1.3
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.10.0-5
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.10.0-4
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.10.0-3
- Release bump for SRP compliance
* Tue May 23 2023 Shivani Agarwal <shivania2@vmware.com> 5.10.0-2
- Bump up version to compile with new gnupg
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.10.0-1
- Automatic Version Bump
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 5.5.1-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 5.5.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.4.5-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 4.2.0-3
- Mass removal python2
* Wed Jan 16 2019 Tapas Kundu <tkundu@vmware.com> 4.2.0-2
- Disabled the make check as the requirements can not be fulfilled
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 4.2.0-1
- Update to version 4.2.0
* Wed Jul 19 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.0-5
- Fixed make check failure
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.0-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-3
- Create pbr3 script
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
- Fix arch
* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.0-1
- Initial packaging for Photon
