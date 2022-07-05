Summary:        Time zone data
Name:           tzdata
Version:        2022a
Release:        1%{?dist}
URL:            http://www.iana.org/time-zones
License:        Public Domain
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.iana.org//time-zones/repository/releases/%{name}%{version}.tar.gz
%define sha512  tzdata=542e4559beac8fd8c4af7d08d816fd12cfe7ffcb6f20bba4ff1c20eba717749ef96e5cf599b2fe03b5b8469c0467f8cb1c893008160da281055a123dd9e810d9
BuildArch:      noarch
%define blddir  %{name}-%{version}

%description
Sources for time zone and daylight saving time data

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
cp -v zone.tab iso3166.tab zone1970.tab $ZONEINFO
zic -d $ZONEINFO -p America/New_York
install -vdm 755 %{buildroot}%{_sysconfdir}
ln -svf %{_datarootdir}/zoneinfo/UTC %{buildroot}%{_sysconfdir}/localtime

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/localtime
%{_datadir}/*

%changelog
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 2022a-1
-   Automatic Version Bump
*   Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 2020a-1
-   Automatic Version Bump
*   Fri Oct 18 2019 Gerrit Photon <photon-checkins@vmware.com> 2019c-1
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
-   Initial build. First version.
