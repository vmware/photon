Summary:  	xinetd -- A better inetd.
Name:		xinetd
Version:	2.3.15
Release:	3%{?dist}
License:	BSD
Group:		System Environment/Daemons
Vendor:     	VMware, Inc.
Distribution: 	Photon
Source0:	%{name}-%{version}.tar.gz
%define sha1 xinetd=168d54aeb181e271e68f4c53847c3e6b2574dba6
Source1:        xinetd.service

BuildRequires:  systemd
Requires:       systemd

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

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/etc/xinetd.d

%makeinstall  
install -m 0600 contrib/xinetd.conf %{buildroot}/etc/
cp contrib/xinetd.d/* %{buildroot}/etc/xinetd.d
mkdir -p %{buildroot}/lib/systemd/system
cp %{SOURCE1} %{buildroot}/lib/systemd/system/xinetd.service

%clean
rm -rf %{buildroot}

%post
%{_sbindir}/ldconfig 
if [ $1 -eq 1 ] ; then
    # Initial installation
    # Enabled by default per "runs once then goes away" exception
    /bin/systemctl enable xinetd.service     >/dev/null 2>&1 || :
fi

%preun
/bin/systemctl disable xinetd.service

%files
%defattr(-, root, root)
%doc CHANGELOG COPYRIGHT README xinetd/sample.conf contrib/empty.conf 
%{_sbindir}/*
%{_datadir}/man/*/*
%attr(0750, root, root) %config(noreplace) /etc/xinetd.conf
%attr(0750, root, root) %config(noreplace) /etc/xinetd.d/*
/lib/systemd/system/xinetd.service

%changelog
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  2.3.15-3
-   Add systemd to Requires and BuildRequires.
*   Thu Dec 03 2015 Xiaolin Li  <xiaolinl@vmware.com> 2.3.15-2
-   Remove rc files
*   Fri Aug 07 2015 Xiaolin Li  <xiaolinl@vmware.com> 2.3.15-1
-   Add xinetd library to photon
*   Sun Sep 07 2003 Steve Grubb <linux_4ever@yahoo.com>
-   Refined installation and added services.
 
