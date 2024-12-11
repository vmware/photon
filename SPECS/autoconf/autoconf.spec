Summary:        The package automatically configure source code
Name:           autoconf
Version:        2.71
Release:        6%{?dist}
URL:            http://www.gnu.org/software/autoconf
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/autoconf/%{name}-%{version}.tar.xz
%define sha512 %{name}=73d32b4adcbe24e3bafa9f43f59ed3b6efbd3de0f194e5ec90375f35da1199c583f5d3e89139b7edbad35171403709270e339ffa56a2ecb9b3123e9285021ff0

Source1: license.txt
%include %{SOURCE1}

Requires:       perl
Requires:       m4

BuildRequires:  m4

BuildArch:      noarch

Provides: autoconf213
Obsoletes: autoconf213

%description
The package contains programs for producing shell scripts that can
automatically configure source code.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%check
make -k check %{?_smp_mflags} TESTSUITEFLAGS="1-500"

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/autoconf/*

%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.71-6
- Release bump for SRP compliance
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.71-5
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.71-4
- Release bump for SRP compliance
* Tue Dec 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.71-3
- Add provides & obsoletes autoconf213
* Thu Nov 10 2022 Dweep Advani <dadvani@vmware.com> 2.71-2
- Rebuild with perl 5.36.0
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2.71-1
- Automatic Version Bump
* Sun Nov 15 2020 Prashant Singh Chauhan <psinghchauha@vmware.com> 2.69-9
- Fix for make check failure port test to bash 5.0
* Wed Sep 11 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 2.69-8
- Fix for make check failure
* Wed Oct 17 2018 Dweep Advani <dadvani@vmware.com> 2.69-7
- Build section is changed to used %configure
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.69-6
- Fix arch
* Tue Dec 6 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.69-5
- Fixed Bug 1718089 make check failure
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.69-4
- GA - Bump release of all rpms
* Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 2.69-3
- Adding m4 package to build and run time required package
* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.69-2
- Adding perl packages to required packages
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.69-1
- Initial build.  First version
