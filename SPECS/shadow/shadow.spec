Summary:	Programs for handling passwords in a secure way
Name:		shadow
Version:	4.2.1
Release:	10%{?dist}
URL:		http://pkg-shadow.alioth.debian.org/
License:	BSD
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://pkg-shadow.alioth.debian.org/releases/%{name}-%{version}.tar.xz
%define sha1 shadow=0917cbadd4ce0c7c36670e5ecd37bbed92e6d82d
Source1:	PAM-Configuration-Files-1.5.tar.gz
%define sha1 PAM=08052511f985e3b3072c194ac1287e036d9299fb
Patch0: chkname-allowcase.patch   
BuildRequires: 	cracklib
BuildRequires: 	cracklib-devel
Requires:   	cracklib
Requires:   	cracklib-dicts
BuildRequires:	Linux-PAM
Requires:	Linux-PAM

%description
The Shadow package contains programs for handling passwords
in a secure way.

%package lang
Summary: Additional language files for shadow
Group:		Applications/System
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of shadow.

%prep
%setup -q -n %{name}-%{version}
%setup -q -T -D -a 1
%patch0 -p1
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

sed -i "s/^PASS_MAX_DAYS.*/PASS_MAX_DAYS    90/" %{buildroot}/etc/login.defs

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

%check
make %{?_smp_mflags} check

%post
%{_sbindir}/pwconv
%{_sbindir}/grpconv

%files
%defattr(-,root,root)
%config(noreplace) /etc/login.defs
%config(noreplace) /etc/login.access
%config(noreplace) /etc/default/useradd
%config(noreplace) /etc/limits
/bin/*
/sbin/nologin
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1
%{_mandir}/man5
%{_mandir}/man8
%exclude %{_mandir}/cs
%exclude %{_mandir}/da
%exclude %{_mandir}/de
%exclude %{_mandir}/fi
%exclude %{_mandir}/fr
%exclude %{_mandir}/hu
%exclude %{_mandir}/id
%exclude %{_mandir}/it
%exclude %{_mandir}/ja
%exclude %{_mandir}/ko
%exclude %{_mandir}/man3
%exclude %{_mandir}/pl
%exclude %{_mandir}/pt_BR
%exclude %{_mandir}/ru
%exclude %{_mandir}/sv
%exclude %{_mandir}/tr
%exclude %{_mandir}/zh_CN
%exclude %{_mandir}/zh_TW
%config(noreplace) %{_sysconfdir}/pam.d/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.1-10
-   Added -lang subpackage
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 4.2.1-9
-   Modified %check
*   Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-8
-   Added logic to not replace pam.d conf files in upgrade scenario
*   Fri May 27 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-7
-   Adding pam_cracklib module as requisite to pam password configuration
*   Wed May 25 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-6
-   Modifying pam_systemd module as optional in a session
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-5
-   GA - Bump release of all rpms
*   Mon May 2 2016 Xiaolin Li <xiaolinl@vmware.com> 4.2.1-4
-   Enabling pam_systemd module in a session.
*   Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-3
-   Setting password aging limits to 90 days
*   Wed Apr 27 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-3
-   Setting password aging limits to 365 days
*   Wed Mar 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-2
-   Enabling pam_limits module in a session
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 4.2.1-1
-   Update version
*   Wed Dec 2 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-6
-   Fixed PAM Configuration file for passwd
*   Mon Oct 26 2015 Sharath George <sharathg@vmware.com> 4.1.5.1-5
-   Allow mixed case in username.
*   Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-4
-   Fixed PAM Configuration file for chpasswd
*   Tue Jun 16 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.5.1-3
-   Use group id 100(users) by default
*   Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-2
-   Adding PAM support
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-1
-   Initial build. First version
