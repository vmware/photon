Summary:	Time zone data
Name:		tzdata
Version:	2013i
Release:	1
URL:		http://www.iana.org/time-zones
License:	Public Domain
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.iana.org//time-zones/repository/releases/%{name}%{version}.tar.gz
BuildArch:	noarch
%description
Sources for time zone and daylight saving time data
%define blddir		%{name}-%{version}
%prep
rm -rf %{blddir}
install -vdm 755 %{blddir}
cd %{blddir}
tar xf %{SOURCE0}
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
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2013i-1
-	Initial build. First version
