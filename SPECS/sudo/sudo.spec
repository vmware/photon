Summary:        Sudo
Name:           sudo
Version:        1.9.5
Release:        1%{?dist}
License:        ISC
URL:            https://www.sudo.ws/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
%define sha1    sudo=1e9fccda4beccca811ecb48866776388c9c377ae
BuildRequires:  man-db
BuildRequires:  Linux-PAM-devel
BuildRequires:  sed
Requires:       Linux-PAM
Requires:       shadow
Patch0:         CVE-2021-3156_1.patch
Patch1:         CVE-2021-3156_2.patch
Patch2:         CVE-2021-3156_3.patch
Patch3:         CVE-2021-3156_4.patch

%description
The Sudo package allows a system administrator to give certain users (or groups of users)
the ability to run some (or all) commands as root or another user while logging the commands and arguments.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure \
    --libexecdir=%{_libdir} \
    --docdir=%{_docdir}/%{name}-%{version} \
    --with-all-insults \
    --with-env-editor \
    --with-pam \
    --with-passprompt="[sudo] password for %p"

make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
find %{buildroot}/%{_libdir} -name '*.so~' -delete
sed -i '/@includedir.*/i \
%wheel ALL=(ALL) ALL \
%sudo   ALL=(ALL) ALL' %{buildroot}/etc/sudoers
install -vdm755 %{buildroot}/etc/pam.d
cat > %{buildroot}/etc/pam.d/sudo << EOF
#%%PAM-1.0
auth       include      system-auth
account    include      system-account
password   include      system-password
session    include      system-session
session    required     pam_env.so
EOF
mkdir -p %{buildroot}%{_libdir}/tmpfiles.d
touch %{buildroot}%{_libdir}/tmpfiles.d/sudo.conf
%find_lang %{name}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
  getent group wheel > /dev/null || groupadd wheel
fi

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files -f %{name}.lang
%defattr(-,root,root)
%attr(0440,root,root) %config(noreplace) %{_sysconfdir}/sudoers
%attr(0640,root,root) %config(noreplace) /etc/sudo.conf
%attr(0640,root,root) %config(noreplace) /etc/sudo_logsrvd.conf
%attr(0750,root,root) %dir %{_sysconfdir}/sudoers.d/
%config(noreplace) %{_sysconfdir}/pam.d/sudo
%{_bindir}/*
%{_includedir}/*
%{_libdir}/sudo/*.so
%{_libdir}/sudo/*.so.*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_docdir}/%{name}-%{version}/*
%{_datarootdir}/locale/*
%attr(0644,root,root) %{_libdir}/tmpfiles.d/sudo.conf
%exclude  /etc/sudoers.dist

%changelog
*   Fri Jan 29 2021 Shreyas B. <shreyasb@vmware.com> 1.9.5-1
-   Upgrade sudo to v1.9.5
*   Thu Jan 21 2021 Tapas Kundu <tkundu@vmware.com> 1.8.30-3
-   Fix CVE-2021-3156
*   Thu Apr 02 2020 Shreyas B. <shreyasb@vmware.com> 1.8.30-2
-   Fix - Set RLIMIT_CORE to zero when it's failed to set to RLIM_INFINITY.
*   Mon Jan 06 2020 Shreyas B. <shreyasb@vmware.com> 1.8.30-1
-   Upgrade sudo to v1.8.30 for fixing the CVE-2019-19232 & CVE-2019-19234.
*   Tue Oct 15 2019 Shreyas B. <shreyasb@vmware.com> 1.8.23-2
-   Fix for CVE-2019-14287.
*   Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 1.8.23-1
-   Update to version 1.8.23.
*   Thu Mar 01 2018 Anish Swaminathan <anishs@vmware.com> 1.8.20p2-5
-   Move includedir sudoers.d to end of sudoers file
*   Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.20p2-4
-   No direct toybox dependency, shadow depends on toybox
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.20p2-3
-   Requires shadow or toybox
*   Fri Jul 07 2017 Chang Lee <changlee@vmware.com> 1.8.20p2-2
-   Including /usr/lib/tmpfiles.d/sudo.conf from %files
*   Thu Jun 15 2017 Kumar Kaushik <kaushikk@vmware.com> 1.8.20p2-1
-   Udating version to 1.8.20p2, fixing CVE-2017-1000367 and CVE-2017-1000368
*   Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.19p2-1
-   Update to version 1.8.19p2
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.18p1-3
-   BuildRequires Linux-PAM-devel
*   Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> 1.8.18p1-2
-   Remove --with-pam-login to use /etc/pam.d/sudo for `sudo -i`
-   Fix groupadd wheel warning during the %post action
*   Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.8.18p1-1
-   Update to 1.8.18p1
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 1.8.15-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-3
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-2
-   Fix for upgrade issues
*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-1
-   Update to 1.8.15-1.
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.8.11p1-5
-   Edit post script.
*   Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-4
-   Fixing permissions on /etc/sudoers file
*   Fri May 29 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-3
-   Adding sudo configuration and PAM config file
*   Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-2
-   Adding PAM support
*   Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-1
-   Initial build.  First version