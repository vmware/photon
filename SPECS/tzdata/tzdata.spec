Summary:        Time zone data
Name:           tzdata
Version:        2023c
Release:        1%{?dist}
URL:            http://www.iana.org/time-zones
License:        Public Domain
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.iana.org//time-zones/repository/releases/%{name}%{version}.tar.gz
%define sha512  tzdata=608bd286ebcbd0004cfdc1da183273f08aff61f90c8867661154453d77a05d421e4c46ad6d066a1fe2e87d5c82ec0f1c0224667a3b35f3180a3eb7f6ff84cbf5
BuildArch:      noarch

%description
Sources for time zone and daylight saving time data
%define blddir      %{name}-%{version}

%prep
rm -rf %{blddir}
install -vdm 755 %{blddir}
cd %{blddir}
tar xf %{SOURCE0} --no-same-owner
%build
%install
cd %{blddir}
ZONEINFO=%{buildroot}%{_datarootdir}/zoneinfo
install -vdm 755 $ZONEINFO/{posix,right}
for tz in etcetera southamerica northamerica europe africa antarctica  \
    asia australasia backward; do
    zic -L /dev/null    -d $ZONEINFO        -y "sh yearistype.sh" ${tz}
    zic -L /dev/null    -d $ZONEINFO/posix  -y "sh yearistype.sh" ${tz}
    zic -L leapseconds  -d $ZONEINFO/right  -y "sh yearistype.sh" ${tz}
done
cp -v zone.tab iso3166.tab zone1970.tab leap-seconds.list $ZONEINFO
zic -d $ZONEINFO -p America/New_York
install -vdm 755 %{buildroot}%{_sysconfdir}
ln -svf %{_datarootdir}/zoneinfo/UTC %{buildroot}%{_sysconfdir}/localtime

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/localtime
%{_datadir}/*

%changelog
*   Fri Jun 30 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2023c-1
-   Update to 2023c
*   Fri Jan 13 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 2020f-2
-   Add leap-seconds.list file
*   Fri Jan 08 2021 Gerrit Photon <photon-checkins@vmware.com> 2020f-1
-   Automatic Version Bump
*   Fri Oct 11 2019 Gerrit Photon <photon-checkins@vmware.com> 2019c-1
-   Automatic Version Bump
*   Fri Aug 16 2019 Gerrit Photon <photon-checkins@vmware.com> 2019b-1
-   Automatic Version Bump
*   Wed May 22 2019 Gerrit Photon <photon-checkins@vmware.com> 2019a-1
-   Automatic Version Bump
*   Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 2017b-3
-   Add zone1970.tab to zoneinfo
*   Mon May 01 2017 Bo Gan <ganb@vmware.com> 2017b-2
-   Remove (pre/post)trans, config file as noreplace.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2017b-1
-   Updated to version 2017b.
*   Wed Dec 14 2016 Anish Swaminathan <anishs@vmware.com> 2016h-2
-   Preserve /etc/localtime symlink over upgrade
*   Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 2016h-1
-   Upgrade to 2016h
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2016a-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2016a-1
-   Upgraded to version 2016a
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2013i-1
-   Initial build. First version
