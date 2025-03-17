Name:           python3-asn1crypto
Version:        1.5.1
Release:        3%{?dist}
Summary:        A fast, pure Python library for parsing and serializing ASN.1 structures.
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/packages/67/14/5d66588868c4304f804ebaff9397255f6ec5559e46724c2496e0f26e68d6/asn1crypto-0.22.0.tar.gz

Source0:        asn1crypto-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3

BuildArch:      noarch

%description
A fast, pure Python library for parsing and serializing ASN.1 structures.

%prep
%autosetup -p1 -n asn1crypto-%{version}

%build
%py3_build

%install
%py3_install

#%%check
#Commented out %check due to no test existence

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.5.1-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.1-2
- Update release to compile with python 3.11
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.1-1
- Update to 1.5.1
* Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.0-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 0.24.0-2
- Removed python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.24.0-1
- Update to version 0.24.0
* Wed Jul 05 2017 Chang Lee <changlee@vmware.com> 0.22.0-3
- Removed %check because the source does not include the test module
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.22.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.22.0-1
- Initial
