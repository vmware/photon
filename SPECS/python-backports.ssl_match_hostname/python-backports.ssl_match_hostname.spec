%define srcname backports.ssl_match_hostname

Name:           python3-backports.ssl_match_hostname
Version:        3.7.0.1
Release:        4%{?dist}
Summary:        Backported python ssl_match_hostname
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/backports.ssl_match_hostname

Source0: https://pypi.python.org/packages/76/21/2dc61178a2038a5cb35d14b61467c6ac632791ed05131dda72c20e7b9e23/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=9048ed093dc8a166a80d16a9aa0e06d36ea43ce7d324818608d25b1ef5057b1c66dd3514f9b35ab13bc60b2e5a3de29e690607e928fac2c9df16506759bd14dd

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description
Backported python ssl_match_hostname feature

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}
rm -f %{buildroot}%{python3_sitelib}/backports/__init__.py*
find %{buildroot}%{python3_sitelib}/ -name '*.pyc' -delete -o \
    -name '*__pycache__' -delete

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.7.0.1-4
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.7.0.1-3
- Update release to compile with python 3.11
* Wed Oct 28 2020 Dweep Advani <dadvani@vmware.com> 3.7.0.1-2
- Fixed install conflicts with python3-configparser
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.7.0.1-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.5.0.1-2
- Mass removal python2
* Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.5.0.1-1
- Initial version of python backports.ssl_match_hostname for PhotonOS.
