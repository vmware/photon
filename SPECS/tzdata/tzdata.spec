Summary:	Time zone data
Name:		tzdata
Version:	2016h
Release:	1%{?dist}
URL:		http://www.iana.org/time-zones
License:	Public Domain
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.iana.org//time-zones/repository/releases/%{name}%{version}.tar.gz
%define sha1 tzdata=2a43fc1665aab340d8d6505dff9f57b270b5dda2
BuildArch:	noarch
%description
Sources for time zone and daylight saving time data
%define sha1 tzdata=0fe77c8cca50b5f20d73e9c2a5b4fadca34c1504
%define blddir		%{name}-%{version}
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
	asia australasia backward pacificnew systemv; do
	zic -L /dev/null	-d $ZONEINFO		-y "sh yearistype.sh" ${tz}
	zic -L /dev/null	-d $ZONEINFO/posix	-y "sh yearistype.sh" ${tz}
	zic -L leapseconds	-d $ZONEINFO/right	-y "sh yearistype.sh" ${tz}
done
cp -v zone.tab iso3166.tab $ZONEINFO
zic -d $ZONEINFO -p America/New_York
install -vdm 755 %{buildroot}%{_sysconfdir}
ln -svf %{_datarootdir}/zoneinfo/UTC %{buildroot}%{_sysconfdir}/localtime
%files
%defattr(-,root,root)
%{_sysconfdir}/localtime
%{_datadir}/*
%changelog
*   	Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 2016h-1
-   	Upgrade to 2016h
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2016a-2
-	GA - Bump release of all rpms
*   	Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2016a-1
-   	Upgraded to version 2016a
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2013i-1
-	Initial build. First version
