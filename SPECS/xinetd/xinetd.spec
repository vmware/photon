Summary:  	xinetd -- A better inetd.
Name:		xinetd
Version:	2.3.15
Release:	1%{?dist}
License:	BSD
URL:		http://www.xinetd.org/
Group:		System Environment/Daemons
Vendor:     	VMware, Inc.
Distribution: 	Photon
Source0:	%{name}-%{version}.tar.gz
%define sha1 xinetd=168d54aeb181e271e68f4c53847c3e6b2574dba6
Source1:        xinetd.service


%description
Xinetd is a powerful inetd replacement. Xinetd has access control 
mechanisms, extensive logging capabilities, the ability to make 
services available based on time, can place limits on the number 
of servers that can be started, and has a configurable defence 
mechanism to protect against port scanners, among other things.
 
%prep
%setup -q

%build
  ./configure \
	--sbindir=%{buildroot}/%{_sbindir} 	\
	--mandir=%{buildroot}/%{_datadir}/man 
  make
  strip xinetd/xinetd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/etc/xinetd.d

%makeinstall  
#install -m 0755 xinetd6 %{buildroot}/%{_sbindir}
install -m 0755 contrib/xinetd %{buildroot}/etc/rc.d/init.d/xinetd
install -m 0600 contrib/xinetd.conf %{buildroot}/etc/
cp contrib/xinetd.d/* %{buildroot}/etc/xinetd.d
#pushd %{buildroot}
mkdir -p %{buildroot}/lib/systemd/system
cp %{SOURCE1} %{buildroot}/lib/systemd/system/xinetd.service
#popd
install -vdm755 %{buildroot}/etc/systemd/system/multi-user.target.wants
ln -sfv ../../../../lib/systemd/system/xinetd.service  %{buildroot}/etc/systemd/system/multi-user.target.wants/xinetd.service
%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig 
%systemd_post xinetd.service

%preun
%systemd_preun xinetd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart xinetd.service

%files
%defattr(-, root, root)
%doc CHANGELOG COPYRIGHT README xinetd/sample.conf contrib/empty.conf 
%{_sbindir}/*
%{_datadir}/man/*/*
%attr(0750, root, root) %config(noreplace) /etc/rc.d/init.d/xinetd
%attr(0750, root, root) %config(noreplace) /etc/xinetd.conf
%attr(0750, root, root) %config(noreplace) /etc/xinetd.d/*
/lib/systemd/system/xinetd.service
/etc/systemd/system/multi-user.target.wants/xinetd.service

%changelog
*   Fri Aug 07 2015 Xiaolin Li  <xiaolinl@vmware.com> 2.3.15-1
-   Initial build. First version
 
