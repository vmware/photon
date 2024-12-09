Summary:    Intltool
Name:       intltool
Version:    0.51.0
Release:    8%{?dist}
URL:        https://freedesktop.org/wiki/Software/intltool
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:    https://launchpad.net/intltool/+download/%{name}-%{version}.tar.gz
%define sha512  %{name}=4c93cb26592ed0b1622d3b7800b5d6622ffa36f58ac73f2ef0bddfab522565fdfb8fa73d81914b9a202f1d62bc995a08960f8adb9f62c86918e75498e85fbfdf

Source1: license.txt
%include %{SOURCE1}

Requires:      XML-Parser

BuildRequires: XML-Parser

BuildArch:     noarch

%description
The Intltool is an internationalization tool used for extracting translatable strings from source files.

%prep
%autosetup -p1

%build

%configure
%make_build

%install
%make_install %{?_smp_mflags}
install -v -Dm644 doc/I18N-HOWTO %{buildroot}%{_docdir}/%{name}-%{version}/I18N-HOWTO

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/I18N-HOWTO
%{_bindir}/*
%{_datadir}/aclocal/intltool.m4
%{_datadir}/intltool/*
%{_mandir}/man8/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 0.51.0-8
- Release bump for SRP compliance
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 0.51.0-7
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.51.0-6
- Release bump for SRP compliance
* Fri Feb 25 2022 Susant Sahani <ssahani@vmware.com> 0.51.0-5
- Rebuild
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 0.51.0-4
- Cross compilation support
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.51.0-3
- Fix arch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.51.0-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com> 0.51.0-1
- Upgrade to 0.51.0
* Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 0.50.2-1
- Initial version
