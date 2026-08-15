%global build_if %{photon_subrelease} >= 91

Name:           python3-pyasn1
Version:        0.6.4
Release:        2%{?dist}
Summary:        Implementation of ASN.1 types and codecs in Python programming language
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/pyasn1/pyasn1

Source0: https://files.pythonhosted.org/packages/source/p/pyasn1/pyasn1-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-wheel
BuildRequires:  python3-build
BuildRequires:  python3-setuptools
BuildRequires:  python3-installer
BuildRequires:  python3-packaging

Requires:       python3

BuildArch:      noarch

%description
This is an implementation of ASN.1 types and codecs in Python programming language.
It has been first written to support particular protocol (SNMP),
but then generalized to be suitable for a wide range of protocols based on ASN.1 specification.

%prep
%autosetup -p1 -n pyasn1-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%if 0%{?with_check}
%check
python3 -m pytest tests/
%endif

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.6.4-2
- Extend to build for 91 and above
* Mon Aug 03 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.6.4-1
- Upgrade to version 0.6.4
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.6.3-2
- Extended to build for subrelease 91 and above
* Tue Mar 31 2026 Mukul Sikka <mukul.sikka@broadcom.com> 0.6.3-1
- Update to 0.6.3
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.4.8-4
- Bump version as a part of python3.14 upgrade
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
