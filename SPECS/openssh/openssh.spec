Summary:	'Free version of the SSH connectivity tools
Name:		openssh
Version:	6.6p1
Release:	3%{?dist}
License:	BSD
URL:		http://openssh.org
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/%{name}-%{version}.tar.gz
%define sha1 openssh=b850fd1af704942d9b3c2eff7ef6b3a59b6a6b6e
Source1:	http://www.linuxfromscratch.org/blfs/downloads/systemd/blfs-systemd-units-20140907.tar.bz2
%define sha1 blfs-systemd-units=713afb3bbe681314650146e5ec412ef77aa1fe33
Patch1:		blfs_systemd_fixes.patch
Requires:	openssl
Requires:	Linux-PAM
Requires: 	shadow
BuildRequires:  openssl-devel
BuildRequires:	Linux-PAM
BuildRequires:  krb5
%description
The OpenSSH package contains ssh clients and the sshd daemon. This is
useful for encrypting authentication and subsequent traffic over a 
network. The ssh and scp commands are secure implementions of telnet 
and rcp respectively.
%prep
%setup -q
tar xf %{SOURCE1}
%patch1 -p0
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc/ssh \
	--datadir=/usr/share/sshd \
	--with-md5-passwords \
	--with-privsep-path=/var/lib/sshd \
    	--with-pam \
	--with-maintype=man \
	--with-kerberos5=/usr
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}/var/lib/sshd
echo "PermitRootLogin no" >> %{buildroot}/etc/ssh/sshd_config
echo "UsePAM yes" >> %{buildroot}/etc/ssh/sshd_config
#	Install daemon script
pushd blfs-systemd-units-20140907
make DESTDIR=%{buildroot} install-sshd
popd
install -vdm755 %{buildroot}/etc/systemd/system/multi-user.target.wants
ln -sfv ../../../../lib/systemd/system/sshd.service  %{buildroot}/etc/systemd/system/multi-user.target.wants/sshd.service
cat << EOF >> %{buildroot}/lib/systemd/system/sshd-keygen.service
[Unit]
Description=Generate sshd host keys
ConditionPathExists=|!/etc/ssh/ssh_host_rsa_key
ConditionPathExists=|!/etc/ssh/ssh_host_ecdsa_key
ConditionPathExists=|!/etc/ssh/ssh_host_ed25519_key
Before=sshd.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/ssh-keygen -A
EOF

ln -sfv ../../../../lib/systemd/system/sshd-keygen.service  %{buildroot}/etc/systemd/system/multi-user.target.wants/sshd-keygen.service

%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post
/sbin/ldconfig
chown -v root:sys /var/lib/sshd
if ! getent group sshd >/dev/null; then
	groupadd -g 50 sshd
fi
if ! getent passwd sshd >/dev/null; then
	useradd -c 'sshd PrivSep' -d /var/lib/sshd -g sshd -s /bin/false -u 50 sshd
fi


%postun
/sbin/ldconfig
if getent passwd sshd >/dev/null; then
	userdel sshd
fi
if getent group sshd >/dev/null; then
	groupdel sshd
fi
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/etc/systemd/system/multi-user.target.wants/*
/etc/ssh/*
/lib/systemd/system/sshd.service
/lib/systemd/system/sshd.socket
/lib/systemd/system/sshd@.service
/lib/systemd/system/sshd-keygen.service
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%attr(700,root,sys)/var/lib/sshd
%changelog
*	Fri Jul 17 2015 Divya Thaluru <dthaluru@vmware.com> 6.6p1-3
-	Enabling ssh-keygen service by default and fixed service file to execute only once.
*	Tue May 19 2015 Sharath George <sharathg@vmware.com> 6.6p1-2
-	Bulding ssh server with kerberos 5.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 6.6p1-1
-	Initial build.	First version
