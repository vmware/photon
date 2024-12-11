Name:           python3-pyasn1
Version:        0.4.8
Release:        3%{?dist}
Summary:        Implementation of ASN.1 types and codecs in Python programming language
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/etingof/pyasn1

Source0: https://github.com/etingof/pyasn1/archive/refs/tags/pyasn1-%{version}.tar.gz
%define sha512 pyasn1=e64e70b325c8067f87ace7c0673149e82fe564aa4b0fa146d29b43cb588ecd6e81b1b82803b8cfa7a17d3d0489b6d88b4af5afb3aa0052bf92e8a1769fe8f7b0

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

BuildArch:      noarch

%description
This is an implementation of ASN.1 types and codecs in Python programming language.
It has been first written to support particular protocol (SNMP),
but then generalized to be suitable for a wide range of protocols based on ASN.1 specification.

%prep
%autosetup -p1 -n pyasn1-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
python3 setup.py test
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.4.8-3
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.4.8-2
- Update release to compile with python 3.11
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 0.4.8-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 0.4.4-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.4.4-1
- Update to version 0.4.4
* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.2.3-1
- Updated to version 0.2.3.
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 0.1.9-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.9-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.1.9-1
- Upgraded to version 0.1.9
* Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
- Added sha1sum
* Fri Mar 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
