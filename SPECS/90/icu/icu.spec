%global build_if %{photon_subrelease} <= 90

Summary:        International Components for Unicode
Name:           icu
Version:        72.1
Release:        3.1.2%{?dist}
URL:            http://www.icu-project.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/unicode-org/icu/archive/refs/tags/%{name}4c-72_1-src.tgz

Source1: license.txt
%include %{SOURCE1}

# tz database 2026e, zoneinfo64.txt from unicode-org/icu maint-78 (ICU-23249)
# https://raw.githubusercontent.com/unicode-org/icu/abab37734357838657ac18797266481553b5ae83/icu4c/source/data/misc/zoneinfo64.txt
Source2: zoneinfo64.txt

# Metazone data matching the zoneinfo64.txt above. It has to be replaced together
# with it: metaZones.res maps a zone and instant to a metazone, and the metazone is
# what supplies the display name. Pairing a 2026e zoneinfo64.res with ICU 72's
# metaZones.res names historical timestamps in zones such as America/Cancun and
# America/Pangnirtung after a metazone whose offset no longer matches, so formatting
# and then parsing such a timestamp shifts it by an hour.
Source3: metaZones.txt

Patch0: CVE-2025-5222.patch

%description
The International Components for Unicode (ICU) package is a mature,
widely used set of C/C++ libraries providing Unicode and Globalization support for software applications.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1 -n %{name}/source

%build
%configure
%make_build

# The release tarball ships prebuilt data (data/in/icudt72l.dat) with an old tz.
# Replace zoneinfo64.res and metaZones.res in it with ones generated from tz 2026e
# and rebuild the data. timezoneTypes.res is deliberately left alone: maint-78 drops
# the CST6CDT/EST5EDT/MST7MDT/PST8PDT aliases that ICU 72 still publishes.
export LD_LIBRARY_PATH=$PWD/lib
mkdir tzout
cp %{SOURCE2} %{SOURCE3} .
bin/genrb -s . -d tzout zoneinfo64.txt metaZones.txt
bin/icupkg -s tzout -a zoneinfo64.res data/in/icudt72l.dat
bin/icupkg -s tzout -a metaZones.res data/in/icudt72l.dat
touch data/in/icudt72l.dat
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
* Wed Oct 14 2026 Alexey Makhalov <alexey.makhalov@broadcom.com> 72.1-3.1.2
- Update tz data to 2026e
- Update metazone data along with the 2026e tz data
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 72.1-3.1.1
- Adjusted to build for subrelease 90
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 72.1-3.1
- Bump after moving to SPECS/91
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
