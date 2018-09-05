Summary:        Commonly used Mail transport agent (MTA)
Name:           sendmail
Version:        8.15.2
Release:        16%{?dist}
URL:            http://www.sendmail.org/
License:        BSD and CDDL1.1 and MIT
Group:          Email/Server/Library
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.vim.org/pub/mail/sendmail/sendmail-r8/sendmail.8.15.2.tar.gz
BuildRequires:	systemd
BuildRequires:  openldap
BuildRequires:  openssl-devel
BuildRequires:  shadow
Requires:       (coreutils or toybox)
Requires:       systemd
Requires:       m4
Requires:       openldap
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
Requires:       /bin/sed
Requires:       (net-tools or toybox)

%define sha1 sendmail=5801d4b06f4e38ef228a5954a44d17636eaa5a16

%description
Sendmail is widely used Mail Transport agent which helps in sending 
email from one system to another. This program helps in movement 
of email from systems to network and is not just a mail client.

%prep

%setup 

%build

cat >> devtools/Site/site.config.m4 << "EOF"
APPENDDEF(`confENVDEF',`-DSTARTTLS -DSASL -DLDAPMAP')
APPENDDEF(`confMAPDEF', `-DLDAPMAP')
APPENDDEF(`confLIBS', `-lssl -lcrypto -lsasl2 -lldap -llber')
APPENDDEF(`confINCDIRS', `-I/usr/include/sasl')
APPENDDEF(`confLIBS', `-lresolv')
define(`confMANGRP',`root')
define(`confMANOWN',`root')
define(`confSBINGRP',`root')
define(`confUBINGRP',`root')
define(`confUBINOWN',`root')
EOF

sed -i 's|/usr/man/man|/usr/share/man/man|' \
    devtools/OS/Linux           &&

cd sendmail                     &&
sh Build                        &&
cd ../cf/cf                     &&
cp generic-linux.mc sendmail.mc &&
sh Build sendmail.cf

%install
groupadd -g 26 smmsp &&
useradd -c "Sendmail Daemon" -g smmsp -d /dev/null \
        -s /bin/false -u 26 smmsp                  &&

cd cf/cf
install -v -d -m755 %{buildroot}/etc/mail &&
sh Build DESTDIR=%{buildroot} install-cf &&

cd ../..            &&
install -v -d -m755 %{buildroot}/usr/bin &&
install -v -d -m755 %{buildroot}/usr/sbin &&
install -v -d -m755 %{buildroot}/usr/share/man/man1 &&
install -v -d -m755 %{buildroot}/usr/share/man/man8 &&
sh Build DESTDIR=%{buildroot} install    &&

install -v -m644 cf/cf/{submit,sendmail}.mc %{buildroot}/etc/mail &&
cp -v -R cf/* %{buildroot}/etc/mail                               &&

install -v -m755 -d %{buildroot}/usr/share/doc/sendmail-8.15.2/{cf,sendmail} &&

install -v -m644 CACerts FAQ KNOWNBUGS LICENSE PGPKEYS README RELEASE_NOTES \
        %{buildroot}/usr/share/doc/sendmail-8.15.2 &&

install -v -m644 sendmail/{README,SECURITY,TRACEFLAGS,TUNING} \
        %{buildroot}/usr/share/doc/sendmail-8.15.2/sendmail &&

install -v -m644 cf/README %{buildroot}/usr/share/doc/sendmail-8.15.2/cf &&

for manpage in sendmail editmap mailstats makemap praliases smrsh
do
    install -v -m644 ${manpage}/${manpage}.8 %{buildroot}/usr/share/man/man8
done &&

install -v -m644 sendmail/aliases.5    %{buildroot}/usr/share/man/man5 &&
install -v -m644 sendmail/mailq.1      %{buildroot}/usr/share/man/man1 &&
install -v -m644 sendmail/newaliases.1 %{buildroot}/usr/share/man/man1 &&
install -v -m644 vacation/vacation.1   %{buildroot}/usr/share/man/man1

mkdir -p %{buildroot}/etc/systemd/system/
mkdir -p %{buildroot}/etc/sysconfig/

cat > %{buildroot}/etc/sysconfig/sendmail <<- "EOF"
DAEMON=yes
QUEUE=1h

EOF


cat > %{buildroot}/etc/systemd/system/sendmail.service <<- "EOF"
[Unit]
Description=Sendmail Mail Transport Agent
Wants=network-online.target
After=network-online.target syslog.target network.target

[Service]
Environment=QUEUE=1h
EnvironmentFile=/etc/sysconfig/sendmail
Type=forking
ExecStart=/usr/sbin/sendmail -bd -q $QUEUE $SENDMAIL_OPTARG

[Install]
WantedBy=multi-user.target

EOF

%check
make -C test check

%pre
if [ $1 -eq 1 ] ; then
groupadd -g 26 smmsp                               &&
useradd -c "Sendmail Daemon" -g smmsp -d /dev/null \
        -s /bin/false -u 26 smmsp                  &&
chmod -v 1777 /var/mail                            &&
install -v -m700 -d /var/spool/mqueue
fi


%post
if [ $1 -eq 1 ] ; then
  echo $(hostname -f) > /etc/mail/local-host-names
  cat > /etc/mail/aliases << "EOF"
postmaster: root
MAILER-DAEMON: root
EOF
  /bin/newaliases

  cd /etc/mail
  m4 m4/cf.m4 sendmail.mc > sendmail.cf

fi

chmod 700 /var/spool/clientmqueue
chown smmsp:smmsp /var/spool/clientmqueue

%systemd_post sendmail.service

%preun
%systemd_preun sendmail.service


%postun
if [ $1 -eq 0 ] ; then
  userdel smmsp
  groupdel smmsp

  rm -rf /etc/mail
fi
%systemd_postun_with_restart sendmail.service

%files
%config(noreplace)%{_sysconfdir}/mail/sendmail.mc
%config(noreplace)%{_sysconfdir}/mail/sendmail.cf
%config(noreplace)%{_sysconfdir}/mail/submit.cf
%config(noreplace)%{_sysconfdir}/mail/submit.mc
%{_sysconfdir}/mail/feature/*
%{_sysconfdir}/mail/hack/*
%{_sysconfdir}/mail/m4/*
%{_sysconfdir}/mail/mailer/*
%{_sysconfdir}/mail/ostype/*
%{_sysconfdir}/mail/sh/*
%{_sysconfdir}/mail/siteconfig/*
%{_sysconfdir}/mail/domain/*
%{_sysconfdir}/mail/README
%{_sysconfdir}/mail/helpfile
%{_sysconfdir}/mail/sendmail.schema
%{_sysconfdir}/mail/statistics
/usr/*
/var/*
/etc/systemd/system/sendmail.service
/etc/sysconfig/sendmail

%exclude /usr/lib/debug
%exclude /usr/src
%exclude /usr/share/man/*
%exclude %{_sysconfdir}/mail/cf/*

%changelog
*   Thu Aug 30 2018 Dheeraj Shetty <dheerajs@vmware.com> 8.15.2-16
-   Remove dependency on libdb
*   Mon Oct 02 2017 Kumar Kaushik <kaushikk@vmware.com> 8.15.2-15
-   Removed duplicate configuration folder.
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 8.15.2-14
-   Requires coreutils/net-tools or toybox, /bin/sed
-   Remove shadow from requires and use explicit tools for post actions
*   Mon Jun 12 2017 Darren Hart (VMware) <dvhart@infradead.org> 8.15.2-13
-   Update the sendmail License meta-data
*   Tue Apr 4 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.15.2-12
-   Update requires to use libdb and build to use libdb-devel
*   Fri Mar 24 2017 Kumar Kaushik <kaushikk@vmware.com> 8.15.2-11
-   Fixing sendmail upgrade config no replace.
*   Mon Mar 06 2017 Kumar Kaushik <kaushikk@vmware.com> 8.15.2-10
-   Adding dependency to start after network-online.
*   Wed Dec 14 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.15.2-9
-   Replace obsoleted dependency inetutils with net-tools
*   Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.15.2-8
-   fix pre script, add coreutils,inetutils,sed,shadow to requires
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 8.15.2-7
-   Modified %check
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> 8.15.2-6
-   Fixed logic to restart the active services after upgrade
*   Wed May 25 2016 Kumar Kaushik <kaushikk@vmware.com> 8.15.2-5
-   Adding dependencies and fixing post section installation bug.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.15.2-4
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.15.2-3
-   Fix for upgrade issues
*   Wed Feb 17 2016 Kumar Kaushik <kaushikk@vmware.com> 8.15.2-2
-   Changing permission and owner of clientmqueue.
*   Tue Jan 05 2016 Kumar Kaushik <kaushikk@vmware.com> 8.15.2-1
-   Initial build.  First version

