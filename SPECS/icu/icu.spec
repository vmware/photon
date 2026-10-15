%global build_if %{photon_subrelease} >= 91

Summary:        International Components for Unicode
Name:           icu
Version:        78.3
Release:        1%{?dist}
URL:            http://www.icu-project.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/unicode-org/icu/releases/download/release-%{version}/%{name}4c-%{version}-sources.tgz

# ICU data sources, the sources tarball only has the prebuilt data (icudt78l.dat)
Source2: https://github.com/unicode-org/icu/releases/download/release-%{version}/%{name}4c-%{version}-data.zip

Source1: license.txt
%include %{SOURCE1}

# tz database 2026e, from maint-78 (ICU-23249, https://github.com/unicode-org/icu/pull/4248)
Patch0: icu-tz-2026e.patch

# configure uses python to generate the data build rules, also used to extract the data zip
BuildRequires:  python3

%description
The International Components for Unicode (ICU) package is a mature,
widely used set of C/C++ libraries providing Unicode and Globalization support for software applications.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -N -n %{name}/source
# build the data from sources instead of using the prebuilt one
rm data/in/icudt*.dat
python3 -m zipfile -e %{SOURCE2} .
# the files in the data zip have CRLF line endings, convert them to LF so the tz patch applies
sed -i 's/\r$//' data/misc/zoneinfo64.txt data/misc/metaZones.txt data/misc/timezoneTypes.txt
%autopatch -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%exclude %dir %{_libdir}/debug
%exclude %{_libdir}/icu

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Oct 14 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 78.3-1
- Upgrade to v78.3 and update tz data to 2026e, remove CVE-2025-5222 patch (fixed upstream)
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 76.1-2
- Extended to build for subrelease 91 and above
* Mon Feb 16 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 76.1-1
- Upgrade as required by mozjs
* Mon Aug 04 2025 Mukul Sikka <mukul.sikka@broadcom.com> 72.1-3
- Fix for CVE-2025-5222
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 72.1-2
- Release bump for SRP compliance
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 72.1-1
- Upgrade to v72.1
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 71.1-1
- Upgrade to v71.1
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 70.1-2
- Fix binary path
* Wed Nov 24 2021 Alexey Makhalov <amakhalov@vmware.com> 70.1-1
- Version update
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 69.1-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 67.1-1
- Automatic Version Bump
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 61.1-1
- Update to latest version
* Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 55.1-1
- Initial build for photon
