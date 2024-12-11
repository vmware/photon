Name:           python3-ipaddr
Version:        2.2.0
Release:        4%{?dist}
Url:            https://github.com/google/ipaddr-py
Summary:        Google's Python IP address manipulation library
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/source/i/ipaddr/ipaddr-%{version}.tar.gz
%define sha512  ipaddr=5adb117c44e6e5dbdb9e96543aa7a34f35b4a4ec9baa163a25448058c34091bf4019d24f0250928291e4d4bc97dcdf75865daef739e2d94f98cc584e6e6c50dd

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
ipaddr.py is a library for working with IP addresses, both IPv4 and IPv6. It was developed by Google for internal use, and is now open source.

%prep
%autosetup -n ipaddr-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 ipaddr_test.py

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.2.0-4
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.0-3
- Update release to compile with python 3.11
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.2.0-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-1
- Update to version 2.2.0
* Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> 2.1.11-4
- Adding python 3 support.
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 2.1.11-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.11-2
- GA - Bump release of all rpms
* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
