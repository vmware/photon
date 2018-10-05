%global security_hardening none
Summary:        A UNIX init scheme with service supervision
Name:           runit
Version:        2.1.2
Release:        4%{?dist}
License:        BSD
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
URL:            http://smarden.org/runit/
Source0:        http://smarden.org/runit/runit-%{version}.tar.gz
%define sha1 runit=398f7bf995acd58797c1d4a7bcd75cc1fc83aa66
Source1:	runit.service
#Patch source: https://github.com/imeyer/runit-rpm
Patch0:		runit-default-service.patch
Patch1:		runit-gen-debug.patch

%description
runit is a cross-platform Unix init scheme with service supervision; a
replacement for sysvinit and other init schemes. It runs on GNU/Linux, *BSD,
Mac OS X, and Solaris, and can easily be adapted to other Unix operating
systems.

%prep
%setup -q -n admin/%{name}-%{version}
%patch0
%patch1

%build
sh package/compile

%install
for i in $(< package/commands) ; do
    install -D -m 0755 command/$i %{buildroot}%{_sbindir}/$i
done
for i in man/*8 ; do
    install -D -m 0755 $i %{buildroot}%{_mandir}/man8/${i##man/}
done
install -d -m 0755 %{buildroot}/etc/service
install -D -m 0750 etc/2 %{buildroot}%{_sbindir}/runsvdir-start
install -D -m 0755 %{SOURCE1} %{buildroot}/lib/systemd/system/runit.service

%check
sh package/check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/*
%{_mandir}/man8/*
/lib/systemd/system/runit.service
%dir /etc/service

%changelog
*	Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-4
-	Ensure non empty debuginfo
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.1.2-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-2
-	GA - Bump release of all rpms
*	Tue Aug 4 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.2-1
-	Initial build


