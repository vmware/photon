%define debug_package %{nil}

Summary:        Domain Name System software
Name:           bind
Version:        9.13.2
Release:        1%{?dist}
License:        Mozilla Public License 2.0
URL:            ftp://ftp.isc.org/isc/bind9
Source0:        ftp://ftp.isc.org/isc/bind9/%{version}/bind-%{version}.tar.gz
%define sha1    bind=bd9c44cd1a19aa100ebd1f9fe94ce47e47e0eca7
Source1:        bind.service
Source2:        bind9
Source3:        named.conf
Source4:        127.0.0
Source5:        root.hints
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libcap-devel
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

%description
BIND is open source software that implements the Domain Name System (DNS) protocol 
for the Internet. It is a reference implementation of those protocols, but it is
also production-grade software, suitable for use in high-volume and high-reliability applications.

%prep

%setup -qn %{name}-%{version}

%build
./configure --prefix=/usr           \
            --sysconfdir=/etc       \
            --localstatedir=/var    \
            --mandir=/usr/share/man \
            --enable-threads        \
            --with-libtool          \
            --bindir=/usr/bin       \
            --sbindir=/usr/sbin     \
            --libexecdir=/usr/lib   \
            --libdir=/usr/lib       \
            --disable-static        &&
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/doc/%{name}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/lib/sysusers.d/
mkdir -p %{buildroot}/usr/lib/tmpfiles.d/
mkdir -p %{buildroot}/usr/share/licenses/bind/
mkdir -p %{buildroot}/usr/share/man/man1/
mkdir -p %{buildroot}/usr/share/man/man5/
mkdir -p %{buildroot}/usr/share/man/man8/
mkdir -p %{buildroot}/var/named/etc/namedb/slave
mkdir -p %{buildroot}/var/named/etc/namedb/pz
mkdir -p %{buildroot}/usr/lib/engines
mkdir -p %{buildroot}/var/run/named
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/etc/default
mkdir -p %{buildroot}/srv/named/etc/namedb/
mkdir -p %{buildroot}/srv/named/etc/namedb/slave
mkdir -p %{buildroot}/srv/named/etc/namedb/pz
mkdir -p %{buildroot}/usr/include/bind9
mkdir -p %{buildroot}/usr/include/irs
mkdir -p %{buildroot}/usr/include/isccfg
mkdir -p %{buildroot}/usr/include/ns
mkdir -p %{buildroot}/usr/include/dst
mkdir -p %{buildroot}/usr/include/dns
mkdir -p %{buildroot}/usr/include/isccc
mkdir -p %{buildroot}/usr/include/isc
mkdir -p %{buildroot}/usr/include/pk11
mkdir -p %{buildroot}/usr/include/pkcs11
mkdir -p %{buildroot}/var/log/
mknod %{buildroot}/srv/named/dev/null c 1 3 &&
mknod %{buildroot}/srv/named/dev/urandom c 1 9 &&
chmod 666 %{buildroot}/srv/named/dev/{null,urandom} &&
touch %{buildroot}/srv/named/managed-keys.bind
chmod 770 %{buildroot}/srv/named/

make install &&
install -v -m755 -d /usr/share/doc/%{name}-%{version}/{arm,misc} &&
install -v -m644    doc/arm/*.html \
                    /usr/share/doc/%{name}-%{version}/arm &&
install -v -m644    doc/misc/{dnssec,ipv6,migrat*,options,rfc-compliance,roadmap,sdb} \
                    /usr/share/doc/%{name}-%{version}/misc

cp LICENSE %{buildroot}/usr/share/licenses/bind/
cp COPYRIGHT %{buildroot}/usr/share/licenses/bind/
cp %{SOURCE1} %{buildroot}/usr/lib/systemd/system/
cp %{SOURCE2} %{buildroot}/etc/default/
cp %{SOURCE3} %{buildroot}/srv/named/etc/
cp %{SOURCE4} %{buildroot}/srv/named/etc/namedb/pz/
cp %{SOURCE5} %{buildroot}/srv/named/etc/namedb/
touch %{buildroot}/srv/named/managed-keys.bind

cp /usr/lib/libisc* %{buildroot}/usr/lib/
cp /usr/lib/libdns* %{buildroot}/usr/lib/
cp /usr/lib/libns.so* %{buildroot}/usr/lib/
cp /usr/lib/libisccfg* %{buildroot}/usr/lib/
cp /usr/lib/libbind9* %{buildroot}/usr/lib/
cp /usr/lib/libirs* %{buildroot}/usr/lib/

cp /usr/bin/dig %{buildroot}/usr/bin/
cp /usr/bin/host %{buildroot}/usr/bin/
cp /usr/bin/nslookup %{buildroot}/usr/bin/
cp /usr/bin/delv %{buildroot}/usr/bin/
cp /usr/bin/arpaname %{buildroot}/usr/bin/
cp /usr/bin/named-rrchecker %{buildroot}/usr/bin/
cp /usr/bin/mdig %{buildroot}/usr/bin/
cp /usr/bin/nsupdate %{buildroot}/usr/bin/
cp /usr/bin/isc-config.sh %{buildroot}/usr/bin/
cp /usr/bin/bind9-config %{buildroot}/usr/bin/

cp /usr/sbin/named %{buildroot}/usr/sbin/
cp /usr/sbin/rndc %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-cds %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-dsfromkey %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-importkey %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-keyfromlabel %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-keygen %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-revoke %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-settime %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-signzone %{buildroot}/usr/sbin/
cp /usr/sbin/dnssec-verify %{buildroot}/usr/sbin/
cp /usr/sbin/named-journalprint %{buildroot}/usr/sbin/
cp /usr/sbin/nsec3hash %{buildroot}/usr/sbin/
cp /usr/sbin/named-checkconf %{buildroot}/usr/sbin/
cp /usr/sbin/named-checkzone %{buildroot}/usr/sbin/
cp /usr/sbin/named-compilezone %{buildroot}/usr/sbin/
cp /usr/sbin/rndc-confgen %{buildroot}/usr/sbin/
cp /usr/sbin/ddns-confgen %{buildroot}/usr/sbin/
cp /usr/sbin/tsig-keygen %{buildroot}/usr/sbin/

cp /usr/share/man/man1/host.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/dig.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/nslookup.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/delv.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/named-rrchecker.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/arpaname.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/mdig.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/nsupdate.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/isc-config.sh.1 %{buildroot}/usr/share/man/man1/
cp /usr/share/man/man1/bind9-config.1 %{buildroot}/usr/share/man/man1/

cp /usr/share/man/man5/named.conf.5 %{buildroot}/usr/share/man/man5/
cp /usr/share/man/man5/rndc.conf.5 %{buildroot}/usr/share/man/man5/

cp /usr/share/man/man8/named.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/rndc.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-dsfromkey.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-cds.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-keyfromlabel.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-importkey.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-settime.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-revoke.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-keygen.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-verify.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/dnssec-signzone.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/named-journalprint.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/nsec3hash.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/named-checkconf.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/named-checkzone.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/named-compilezone.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/rndc-confgen.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/ddns-confgen.8 %{buildroot}/usr/share/man/man8/
cp /usr/share/man/man8/tsig-keygen.8 %{buildroot}/usr/share/man/man8/

cp -R /usr/share/doc/%{name}-%{version}/* %{buildroot}/usr/share/doc/%{name}/

cp -R /usr/include/irs/* %{buildroot}/usr/include/irs/
cp -R /usr/include/bind9/* %{buildroot}/usr/include/bind9/
cp -R /usr/include/isccfg/* %{buildroot}/usr/include/isccfg/
cp -R /usr/include/ns/* %{buildroot}/usr/include/ns/
cp -R /usr/include/dst/* %{buildroot}/usr/include/dst/
cp -R /usr/include/dns/* %{buildroot}/usr/include/dns/
cp -R /usr/include/isccc/* %{buildroot}/usr/include/isccc/
cp -R /usr/include/isc/* %{buildroot}/usr/include/isc/
cp -R /usr/include/pkcs11/* %{buildroot}/usr/include/pkcs11/
cp -R /usr/include/pk11/* %{buildroot}/usr/include/pk11/

cp /etc/bind.keys %{buildroot}/etc/
cp /etc/resolv.conf %{buildroot}/etc/

cp bin/rndc/rndc.conf %{buildroot}/etc/


%post
cp /etc/resolv.conf /etc/resolv.conf.bak
rndc-confgen -a

%pre

groupadd -g 20 named &&
useradd -c "BIND Owner" -g named -s /bin/false -u 20 named &&
install -d -m770 -o named -g named /srv/named

%postun

if [ $1 -eq 0 ] ; then
    /usr/sbin/userdel named
    /usr/sbin/groupdel named
fi

%files
%defattr(-,root,root)
%{_datadir}/
/usr/lib/sysusers.d
/usr/lib/tmpfiles.d
/usr/bin/*
/usr/sbin/*
/usr/lib/*
/etc/bind.keys
/etc/default/bind9
/srv/named/*
/usr/include/bind9/*
/usr/include/irs/*
/usr/include/isccfg/*
/usr/include/ns/*
/usr/include/dst/*
/usr/include/dns/*
/usr/include/isccc/*
/usr/include/isc/*
/usr/include/pk11/*
/usr/include/pkcs11/*
/usr/share/man/*
/usr/share/licenses/bind/*
%attr(775,named,named) /usr/share/doc/%{name}/*
%attr(775,named,named) /srv/named
%attr(775,named,named) /usr/lib/systemd/system/%{name}.service
/etc/resolv.conf
/etc/rndc.conf

%changelog
*   Wed Aug 08 2018 Tapas Kundu <tkundu@vmware.com> 9.13.2-1
-   Initial build. First version
