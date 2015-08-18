Summary:	Network Time Protocol reference implementation
Name:		ntp
Version:	4.2.8p3
Release:	1%{?dist}
License:	NTP
URL:		http://www.ntp.org/
Group:		System Environment/NetworkingPrograms
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/%{name}-%{version}.tar.gz
%define sha1 ntp=fc624396f8d9f9bc282da30c8e8e527ade7d420f
Source1:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20140919.tar.bz2
%define sha1 blfs-bootscripts=762b68f79f84463a6b1dabb69e9dbdc2c43f32d8
Requires:	libcap >= 2.24
BuildRequires:	which
BuildRequires:	libcap
Requires:	shadow

%description
The ntp package contains a client and server to keep the time 
synchronized between various computers over a network. This 
package is the official reference implementation of the 
NTP protocol.
%prep
%setup -q
tar xf %{SOURCE1}
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
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -v -m755	-d %{buildroot}%{_datadir}/doc/%{name}-%{version}
cp -v -R html/*		%{buildroot}%{_datadir}/doc/%{name}-%{version}/
install -vdm 755 %{buildroot}/etc
cat > %{buildroot}/etc/ntp.conf <<- "EOF"
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
#	Install daemon script
pushd blfs-bootscripts-20140919
make DESTDIR=%{buildroot} install-ntpd
popd
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%pre
if ! getent group ntp >/dev/null; then
	groupadd -g 87 ntp
fi
if ! getent passwd ntp >/dev/null; then
	useradd -c "Network Time Protocol" -d /var/lib/ntp -u 87 -g ntp -s /bin/false ntp
fi
%postun
/sbin/ldconfig
if getent passwd ntp >/dev/null; then
	userdel ntp
fi
if getent group ntp >/dev/null; then
	groupdel ntp
fi
%post	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/etc/ntp.conf
/etc/rc.d/init.d/ntpd
/etc/rc.d/rc0.d/K46ntpd
/etc/rc.d/rc1.d/K46ntpd
/etc/rc.d/rc2.d/K46ntpd
/etc/rc.d/rc3.d/S26ntpd
/etc/rc.d/rc4.d/S26ntpd
/etc/rc.d/rc5.d/S26ntpd
/etc/rc.d/rc6.d/K46ntpd
%{_bindir}/*
%{_datadir}/doc/%{name}-%{version}/*
%{_datadir}/doc/ntp/*
%{_datadir}/doc/sntp/*
%{_datadir}/licenses/ntp/LICENSE
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/ntp/lib/NTP/Util.pm
%changelog
*	Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.8p3-1
-	Updating to version 4.2.8p3
*	Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.6p5-1
-	Initial build.	First version
