%global security_hardening none
Summary:        A UNIX init scheme with service supervision
Name:           runit
Version:        2.1.2
Release:        6%{?dist}
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://smarden.org/runit/

Source0: http://smarden.org/runit/runit-%{version}.tar.gz

Source1:    runit.service

Source2: license.txt
%include %{SOURCE2}

#Patch source: https://github.com/imeyer/runit-rpm
Patch0:     runit-default-service.patch
Patch1:     runit-gen-debug.patch

BuildRequires: systemd-rpm-macros

%description
runit is a cross-platform Unix init scheme with service supervision; a
replacement for sysvinit and other init schemes. It runs on GNU/Linux, *BSD,
Mac OS X, and Solaris, and can easily be adapted to other Unix operating
systems.

%prep
%autosetup -p1 -n admin/%{name}-%{version}

%build
sh package/compile

%install
for i in $(< package/commands) ; do
    install -D -m 0755 command/$i %{buildroot}%{_sbindir}/$i
done
for i in man/*8 ; do
    install -D -m 0755 $i %{buildroot}%{_mandir}/man8/${i##man/}
done
install -d -m 0755 %{buildroot}%{_sysconfdir}/service
install -D -m 0750 etc/2 %{buildroot}%{_sbindir}/runsvdir-start
install -D -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/runit.service

%check
sh package/check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/*
%{_mandir}/man8/*
%{_unitdir}/runit.service
%dir %{_sysconfdir}/service

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1.2-6
- Release bump for SRP compliance
* Tue Sep 07 2021 Keerthana K <keerthanak@vmware.com> 2.1.2-5
- Bump up version to compile with new glibc
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-4
- Ensure non empty debuginfo
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.1.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-2
- GA - Bump release of all rpms
* Tue Aug 4 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.2-1
- Initial build
