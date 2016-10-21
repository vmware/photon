Summary:	Sudo
Name:		sudo
Version:	1.8.18p1
Release:	2%{?dist}
License:	ISC
URL:		https://www.kernel.org/pub/linux/libs/pam/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
%define sha1 sudo=2df9c1f68b1101aa600ef428bccda1b4a3090ff3
BuildRequires:	man-db
BuildRequires:	Linux-PAM
Requires:	Linux-PAM
Requires:	shadow
%description
The Sudo package allows a system administrator to give certain users (or groups of users) 
the ability to run some (or all) commands as root or another user while logging the commands and arguments. 

%prep
%setup -q
%build

./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libexecdir=%{_libdir} \
        --docdir=%{_docdir}/%{name}-%{version} \
	--with-all-insults         \
        --with-env-editor          \
	--with-pam                 \
        --with-passprompt="[sudo] password for %p"

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
find %{buildroot}/%{_libdir} -name '*.so~' -delete
cat >> %{buildroot}/etc/sudoers << EOF
%wheel ALL=(ALL) ALL
%sudo   ALL=(ALL) ALL
EOF
install -vdm755 %{buildroot}/etc/pam.d
cat > %{buildroot}/etc/pam.d/sudo << EOF
#%%PAM-1.0
auth       include      system-auth
account    include      system-account
password   include      system-password
session    include      system-session
session    required     pam_env.so
EOF

%find_lang %{name}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
  getent group wheel > /dev/null || groupadd wheel
fi
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files -f %{name}.lang
%defattr(-,root,root)
%attr(0440,root,root) %config(noreplace) %{_sysconfdir}/sudoers
%attr(0750,root,root) %dir %{_sysconfdir}/sudoers.d/
%config(noreplace) %{_sysconfdir}/pam.d/sudo
%{_bindir}/*
%{_includedir}/*
%{_libdir}/sudo/*.so
%{_libdir}/sudo/*.so.*
%{_sbindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_docdir}/%{name}-%{version}/*
%{_datarootdir}/locale/*
%changelog
*	Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> 1.8.18p1-2
-	Remove --with-pam-login to use /etc/pam.d/sudo for `sudo -i`
-	Fix groupadd wheel warning during the %post action
*	Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.8.18p1-1
-	Update to 1.8.18p1
*       Mon Oct 04 2016 ChangLee <changlee@vmware.com> 1.8.15-4
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-3
-	GA - Bump release of all rpms
*   	Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-2
-   	Fix for upgrade issues
*	Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-1
-	Update to 1.8.15-1.
*	Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.8.11p1-5
-	Edit post script.
*	Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-4
-	Fixing permissions on /etc/sudoers file
*	Fri May 29 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-3
-	Adding sudo configuration and PAM config file
*	Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-2
-	Adding PAM support
*	Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-1
-	Initial build.	First version
