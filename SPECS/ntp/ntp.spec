Summary:	Network Time Protocol reference implementation
Name:		ntp
Version:	4.2.8p6
Release:	1%{?dist}
License:	NTP
URL:		http://www.ntp.org/
Group:		System Environment/NetworkingPrograms
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/%{name}-%{version}.tar.gz
%define sha1 ntp=7244b0fb66ceb66283480e8f83a4c4a2099f9cd7

#https://github.com/darkhelmet/ntpstat
Source1: ntpstat-master.zip
%define sha1 ntpstat=729cf2c9f10da43554f26875e91e1973d4498761

BuildRequires:	which
BuildRequires:	libcap-devel
BuildRequires:	unzip
BuildRequires:  systemd
Requires:       systemd
Requires:	shadow
Requires:	libcap >= 2.24
%description
The ntp package contains a client and server to keep the time 
synchronized between various computers over a network. This 
package is the official reference implementation of the 
NTP protocol.

%package -n	ntpstat
Summary:	Utilities
Group:      Utilities
%description -n ntpstat
ntpstat is a utility which reports the synchronisation
state of the NTP daemon running on the local machine.

%prep
%setup -q -a 1

%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--sysconfdir=/etc \
	--with-binsubdir=sbin \
	--enable-linuxcaps
make %{?_smp_mflags}
make -C ntpstat-master CFLAGS="$CFLAGS"
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -v -m755	-d %{buildroot}%{_datadir}/doc/%{name}-%{version}
cp -v -R html/*		%{buildroot}%{_datadir}/doc/%{name}-%{version}/
install -vdm 755 %{buildroot}/etc

pushd ntpstat-master
install -m 755 ntpstat %{buildroot}/%{_bindir}
install -m 644 ntpstat.1 %{buildroot}/%{_mandir}/man8/ntpstat.8
popd

cat > %{buildroot}/etc/ntp.conf <<- "EOF"
server scrootdc02.vmware.com
# Asia
server 0.asia.pool.ntp.org
# Australia
server 0.oceania.pool.ntp.org
# Europe
server 0.europe.pool.ntp.org
# North America
server 0.north-america.pool.ntp.org
# South America
server 2.south-america.pool.ntp.org
driftfile /var/cache/ntp.drift
pidfile   /var/run/ntpd.pid
EOF
install -D -m644 COPYRIGHT %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
rm -rf %{buildroot}/etc/rc.d/*

%{_fixperms} %{buildroot}/*
mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/ntpd.service
[Unit]
Description=Network Time Service
After=syslog.target network.target
Documentation=man:ntpd
Conflicts=systemd-timesyncd.service

[Service]
Type=forking
ExecStart=/usr/bin/ntpd -g -u ntp:ntp
PrivateTmp=true

[Install]

WantedBy=multi-user.target
EOF
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%pre
if ! getent group ntp >/dev/null; then
	groupadd -g 87 ntp
fi
if ! getent passwd ntp >/dev/null; then
	useradd -c "Network Time Protocol" -d /var/lib/ntp -u 87 -g ntp -s /bin/false ntp
fi
%post
%{_sbindir}/ldconfig 
if [ $1 -eq 1 ] ; then
    # Initial installation
    # Enabled by default per "runs once then goes away" exception
    /bin/systemctl enable ntpd.service     >/dev/null 2>&1 || :
fi

%preun
/bin/systemctl disable ntpd.service

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%attr(0750, root, root) %config(noreplace) /etc/ntp.conf
/lib/systemd/system/ntpd.service
%exclude %{_bindir}/ntpstat
%exclude %{_mandir}/man8/ntpstat.8*
%{_bindir}/*
%{_datadir}/doc/%{name}-%{version}/*
%{_datadir}/doc/ntp/*
%{_datadir}/doc/sntp/*
%{_datadir}/licenses/ntp/LICENSE
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/ntp/lib/NTP/Util.pm

%files -n ntpstat
%defattr(-,root,root)
%{_bindir}/ntpstat
%{_mandir}/man8/ntpstat.8*

%changelog
*	Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 4.2.8p6-1
-	Upgrade version
*   	Thu Jan 7 2016 Xiaolin Li <xiaolinl@vmware.com>  4.2.8p3-4
-   	Add ntpstat package.
*   	Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  4.2.8p3-3
-   	Add systemd to Requires and BuildRequires.
*	Fri Oct 30 2015 Xiaolin Li <xiaolinl@vmware.com> 4.2.8p3-2
-   	Add ntpd to systemd service.
*	Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.8p3-1
-	Updating to version 4.2.8p3
*	Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.6p5-1
-	Initial build.	First version
