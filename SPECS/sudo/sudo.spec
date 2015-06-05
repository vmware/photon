Summary:	Sudo
Name:		sudo
Version:	1.8.11p1
Release:	3%{?dist}
License:	ISC
URL:		https://www.kernel.org/pub/linux/libs/pam/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
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
	--with-pam-login	   \
        --with-passprompt="[sudo] password for %p"

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
groupadd wheel
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files -f %{name}.lang
%defattr(-,root,root)
%{_sysconfdir}/*
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
*	Fri May 29 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-3
-	Adding sudo configuration and PAM config file
*	Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-2
-	Adding PAM support
*	Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-1
-	Initial build.	First version
