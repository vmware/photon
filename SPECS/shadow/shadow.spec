Summary:	Programs for handling passwords in a secure way
Name:		shadow
Version:	4.1.5.1
Release:	4%{?dist}
URL:		http://pkg-shadow.alioth.debian.org/
License:	BSD
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://cdn.debian.net/debian/pool/main/s/%{name}/%{name}_%{version}.orig.tar.gz
%define sha1 shadow=6e4de75de58405d21b0377b926ae770afccd95bc
Source1:	PAM-Configuration-Files-1.0.tar.gz
%define sha1 PAM=018667e773afb7a6fafb03a1967202dbe9b7f232
BuildRequires: 	cracklib
BuildRequires: 	cracklib-devel
Requires:   	cracklib
Requires:   	cracklib-dicts
BuildRequires:	Linux-PAM
Requires:	Linux-PAM

%description
The Shadow package contains programs for handling passwords
in a secure way.
%prep
%setup -q -n %{name}-%{version}
%setup -q -T -D -a 1
sed -i 's/groups$(EXEEXT) //' src/Makefile.in
find man -name Makefile.in -exec sed -i 's/groups\.1 / /' {} \;
sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' \
	-e 's@/var/spool/mail@/var/mail@' etc/login.defs

sed -i 's@DICTPATH.*@DICTPATH\t/usr/share/cracklib/pw_dict@' \
    etc/login.defs

%build
./configure \
	--sysconfdir=/etc \
	--with-libpam \
    	--with-libcrack \
	--with-group-name-max-length=32

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/passwd %{buildroot}/bin
sed -i 's/yes/no/' %{buildroot}/etc/default/useradd
# Use group id 100(users) by default
sed -i 's/GROUP.*/GROUP=100/' %{buildroot}/etc/default/useradd
# Disable usergroups. Use "users" group by default (see /etc/default/useradd)
# for all nonroot users.
sed -i 's/USERGROUPS_ENAB.*/USERGROUPS_ENAB no/' %{buildroot}/etc/login.defs
cp etc/{limits,login.access} %{buildroot}/etc
for FUNCTION in FAIL_DELAY               \
                FAILLOG_ENAB             \
                LASTLOG_ENAB             \
                MAIL_CHECK_ENAB          \
                OBSCURE_CHECKS_ENAB      \
                PORTTIME_CHECKS_ENAB     \
                QUOTAS_ENAB              \
                CONSOLE MOTD_FILE        \
                FTMP_FILE NOLOGINS_FILE  \
                ENV_HZ PASS_MIN_LEN      \
                SU_WHEEL_ONLY            \
                CRACKLIB_DICTPATH        \
                PASS_CHANGE_TRIES        \
                PASS_ALWAYS_WARN         \
                CHFN_AUTH ENCRYPT_METHOD \
                ENVIRON_FILE
do
    sed -i "s/^${FUNCTION}/# &/" %{buildroot}/etc/login.defs
done
pushd PAM-Configuration-Files
install -vm644 * %{buildroot}%{_sysconfdir}/pam.d/
popd
for PROGRAM in chfn chgpasswd chsh groupadd groupdel \
               groupmems groupmod newusers useradd userdel usermod
do
    install -v -m644 %{buildroot}%{_sysconfdir}/pam.d/chage %{buildroot}%{_sysconfdir}/pam.d/${PROGRAM}
    sed -i "s/chage/$PROGRAM/" %{buildroot}%{_sysconfdir}/pam.d/${PROGRAM}
done
%find_lang %{name}
%post
%{_sbindir}/pwconv
%{_sbindir}/grpconv
%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) /etc/login.defs
%config(noreplace) /etc/login.access
%config(noreplace) /etc/default/useradd
%config(noreplace) /etc/limits
/bin/*
/sbin/nologin
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*/*
%{_sysconfdir}/pam.d/*
%changelog
*	Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-4
-	Fixed PAM Configuration file for chpasswd
*	Tue Jun 16 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.5.1-3
-	Use group id 100(users) by default
*	Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-2
-	Adding PAM support
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-1
-	Initial build.	First version
