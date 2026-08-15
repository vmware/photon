%global build_if %{photon_subrelease} >= 91

%define srcname python-ldap

Summary:        Python interface to LDAP
Name:           python3-ldap
Version:        3.4.7
Release:        2%{?dist}
Url:            https://www.python-ldap.org/
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/python-ldap/python-ldap/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-setuptools
BuildRequires:  python3-packaging
BuildRequires:  openldap-devel

Requires:   python3
Requires:   openldap
Requires:   python3-pyasn1
Requires:   python3-pyasn1-modules

%description
python-ldap provides an object-oriented API to access LDAP directory servers from Python programs. It wraps the OpenLDAP client libraries (libldap) via a C extension module and mainly covers the LDAPv3 protocol as specified by RFC 4510 to 4519 (also affects LDAPv2 compatibility). It also provides modules for other LDAP-related operations (e.g. LDIF, LDAPURLs, LDAP schema handling).

%prep
%autosetup -n %{srcname}-%{srcname}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.4.7-2
- Extend to build for 91 and above
* Tue Jul 07 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.4.7-1
- Initial packaging for Photon, subrelease >= 92
