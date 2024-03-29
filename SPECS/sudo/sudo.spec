Summary:        Sudo
Name:           sudo
Version:        1.9.14p3
Release:        2%{?dist}
License:        ISC
URL:            https://www.sudo.ws
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
%define sha512  %{name}=d4af836e3316c35d8b81a2c869ca199e8f2d5cb26dbd98b8ad031f29be62b154452afdf5a506ddabad21b80e5988a49f1f7c8f1ec44718ffcbd7e89ccbdef612
Source1:        %{name}.sysusers

BuildRequires:  man-db
BuildRequires:  Linux-PAM-devel
BuildRequires:  sed
BuildRequires:  systemd-rpm-macros

Requires:       Linux-PAM
Requires:       shadow

%description
The Sudo package allows a system administrator to give certain users (or groups of users)
the ability to run some (or all) commands as root or another user while logging the commands and arguments.

%prep
%autosetup -p1

%build
%configure --host=%{_host} --build=%{_build} \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --program-prefix= \
    --disable-dependency-tracking \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --libdir=%{_libdir} \
    --docdir=%{_docdir}/%{name}-%{version} \
    --with-all-insults \
    --with-env-editor \
    --with-pam \
    --with-passprompt="[sudo] password for %p"

%make_build

%install
%make_install %{?_smp_mflags}
install -v -dm755 %{buildroot}%{_docdir}/%{name}-%{version}
find %{buildroot}%{_libdir} -name '*.so~' -delete
sed -i '/@includedir.*/i \
%wheel ALL=(ALL) ALL \
%sudo   ALL=(ALL) ALL' %{buildroot}%{_sysconfdir}/sudoers
install -vdm755 %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/sudo << EOF
#%%PAM-1.0
auth       include      system-auth
account    include      system-account
password   include      system-password
session    include      system-session
session    required     pam_env.so
EOF
mkdir -p %{buildroot}%{_tmpfilesdir}
touch %{buildroot}%{_tmpfilesdir}/sudo.conf
%find_lang %{name}
%{_fixperms} %{buildroot}/*
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
  %sysusers_create_compat %{SOURCE1}
fi

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files -f %{name}.lang
%defattr(-,root,root)
%attr(0440,root,root) %config(noreplace) %{_sysconfdir}/sudoers
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sudo.conf
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sudo_logsrvd.conf
%attr(0750,root,root) %dir %{_sysconfdir}/sudoers.d/
%config(noreplace) %{_sysconfdir}/pam.d/sudo
%{_bindir}/*
%{_datadir}/locale/*
%{_includedir}/*
%{_sbindir}/*
%{_libexecdir}/sudo/*.so
%{_libexecdir}/sudo/*.so.*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_docdir}/%{name}-%{version}/*
%attr(0644,root,root) %{_tmpfilesdir}/sudo.conf
%exclude %{_sysconfdir}/sudoers.dist
%{_sysusersdir}/%{name}.sysusers

%changelog
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.9.14p3-2
- Resolving systemd-rpm-macros for group creation
* Mon Jul 31 2023 Mukul Sikka <msikka@vmware.com> 1.9.14p3-1
- Version update
* Wed Jan 18 2023 Shivani Agarwal <shivania2@vmware.com> 1.9.12p1-2
- Fix CVE-2023-22809
* Mon Dec 05 2022 Anmol Jain <anmolja@vmware.com> 1.9.12p1-1
- Version Bump
* Wed Oct 12 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.9.11p3-1
- Fix build with latest toolchain
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.9.11-1
- Automatic Version Bump
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.9.10-1
- Automatic Version Bump
* Fri Jan 29 2021 Shreyas B. <shreyasb@vmware.com> 1.9.5-1
- Upgrade sudo to v1.9.5
* Thu Jan 21 2021 Tapas Kundu <tkundu@vmware.com> 1.8.30-3
- Fix CVE-2021-3156
* Thu Apr 02 2020 Shreyas B. <shreyasb@vmware.com> 1.8.30-2
- Fix - Set RLIMIT_CORE to zero when it's failed to set to RLIM_INFINITY.
* Mon Jan 06 2020 Shreyas B. <shreyasb@vmware.com> 1.8.30-1
- Upgrade sudo to v1.8.30 for fixing the CVE-2019-19232 & CVE-2019-19234.
* Tue Oct 15 2019 Shreyas B. <shreyasb@vmware.com> 1.8.23-2
- Fix for CVE-2019-14287.
* Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 1.8.23-1
- Update to version 1.8.23.
* Thu Mar 01 2018 Anish Swaminathan <anishs@vmware.com> 1.8.20p2-5
- Move includedir sudoers.d to end of sudoers file
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.20p2-4
- No direct toybox dependency, shadow depends on toybox
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.20p2-3
- Requires shadow or toybox
* Fri Jul 07 2017 Chang Lee <changlee@vmware.com> 1.8.20p2-2
- Including /usr/lib/tmpfiles.d/sudo.conf from %files
* Thu Jun 15 2017 Kumar Kaushik <kaushikk@vmware.com> 1.8.20p2-1
- Udating version to 1.8.20p2, fixing CVE-2017-1000367 and CVE-2017-1000368
* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.19p2-1
- Update to version 1.8.19p2
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.8.18p1-3
- BuildRequires Linux-PAM-devel
* Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> 1.8.18p1-2
- Remove --with-pam-login to use /etc/pam.d/sudo for `sudo -i`
- Fix groupadd wheel warning during the %post action
* Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.8.18p1-1
- Update to 1.8.18p1
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 1.8.15-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-3
- GA - Bump release of all rpms
* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-2
- Fix for upgrade issues
* Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-1
- Update to 1.8.15-1.
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.8.11p1-5
- Edit post script.
* Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-4
- Fixing permissions on /etc/sudoers file
* Fri May 29 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-3
- Adding sudo configuration and PAM config file
* Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-2
- Adding PAM support
* Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-1
- Initial build.  First version.
