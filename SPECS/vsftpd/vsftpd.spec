Summary:        Very secure and very small FTP daemon.
Name:           vsftpd
Version:        3.0.5
Release:        5%{?dist}
URL:            https://security.appspot.com/vsftpd.html
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://security.appspot.com/downloads/%{name}-%{version}.tar.gz
Source1: %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}
Patch0: add-debug-symbols-to-build.patch
Patch1: fix-libssl-link.patch

BuildRequires: libcap-devel
BuildRequires: Linux-PAM-devel
BuildRequires: openssl-devel
BuildRequires: libnsl-devel
BuildRequires: systemd-devel

Requires: libcap
Requires: Linux-PAM
Requires: openssl
Requires: libnsl
Requires: systemd-rpm-macros

%description
Very secure and very small FTP daemon.

%prep
%autosetup -p1

%build
sed -i 's/#undef VSF_BUILD_SSL/#define VSF_BUILD_SSL/g' builddefs.h
sed -i -e 's|#define VSF_SYSDEP_HAVE_LIBCAP|//&|' sysdeputil.c
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS=""

%install
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/{man5,man8}
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vm 755 %{name} %{buildroot}%{_sbindir}/%{name}
install -vm 644 %{name}.8 %{buildroot}%{_mandir}/man8/
install -vm 644 %{name}.conf.5 %{buildroot}%{_mandir}/man5/
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

cat >> %{buildroot}%{_sysconfdir}/%{name}.conf << "EOF"
background=YES
listen=YES
nopriv_user=%{name}
secure_chroot_dir=%{_datadir}/%{name}/empty
pasv_enable=Yes
pasv_min_port=40000
pasv_max_port=40100
#allow_writeable_chroot=YES
#write_enable=YES
#local_umask=022
#anon_upload_enable=YES
#anon_mkdir_write_enable=YES
EOF

%post
if [ $1 -ge 1 ]; then
  install -vdm 0755 %{_datadir}/%{name}/empty
  install -vdm 0755 /home/ftp
  %sysusers_create_compat %{SOURCE1}
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/*
%{_sbindir}/*
%{_datadir}/*
%{_sysusersdir}/%{name}.sysusers

%changelog
* Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 3.0.5-5
- Release bump for SRP compliance
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 3.0.5-4
- Use systemd-rpm-macros for user creation
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.5-3
- Bump version as a part of libnsl upgrade
* Wed Apr 06 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.5-2
- Fix spec issues
* Fri Feb 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.5-1
- Upgrade to v3.0.5
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.3-7
- Bump up release for openssl
* Tue Aug 04 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.3-6
- Fix openssl-1.1.1 compatibility issue
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 3.0.3-5
- Use libnsl instead of obsoleted nsl from glibc
* Thu Mar 15 2018 Xiaolin Li <xiaolinl@vmware.com> 3.0.3-4
- Enable ssl support.
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.3-3
- Ensure non empty debuginfo
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.3-2
- BuildRequires Linux-PAM-devel
* Wed Nov 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.0.3-1
- Upgraded to version 3.0.3, fixes CVE-2015-1419
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.2-3
- GA - Bump release of all rpms
* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.2-2
- Fix for upgrade issues
* Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 3.0.2-1
- initial version
