# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:        Very secure and very small FTP daemon.
Name:           vsftpd
Version:        3.0.3
Release:        2%{?dist}
License:        GPLv2 with exceptions
URL:            https://security.appspot.com/vsftpd.html
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://security.appspot.com/downloads/%{name}-%{version}.tar.gz
%define sha1    vsftpd=d5f5a180dbecd0fbcdc92bf0ba2fc001c962b55a
BuildRequires:  libcap-devel Linux-PAM openssl-devel vim curl
Requires:       libcap Linux-PAM openssl
%description
Very secure and very small FTP daemon.
%prep
%setup -q
%build
sed -i 's/#undef VSF_BUILD_SSL/#define VSF_BUILD_SSL/g' builddefs.h
sed -i -e 's|#define VSF_SYSDEP_HAVE_LIBCAP|//&|' sysdeputil.c
make %{?_smp_mflags}
%install
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/{man5,man8}
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vm 755 vsftpd        %{buildroot}%{_sbindir}/vsftpd
install -vm 644 vsftpd.8      %{buildroot}%{_mandir}/man8/
install -vm 644 vsftpd.conf.5 %{buildroot}%{_mandir}/man5/
cat >> %{buildroot}/etc/vsftpd.conf << "EOF"
background=YES
listen=YES
nopriv_user=vsftpd
secure_chroot_dir=/usr/share/vsftpd/empty
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
if [ $1 -eq 1 ] ; then
  install -v -d -m 0755 %{_datadir}/vsftpd/empty
  install -v -d -m 0755 /home/ftp
  if ! getent group vsftpd >/dev/null; then
      groupadd -g 47 vsftpd
  fi
  if ! getent group ftp >/dev/null; then
      groupadd -g 45 ftp
  fi
  if ! getent passwd vsftpd >/dev/null; then
      useradd -c "vsftpd User"  -d /dev/null -g vsftpd -s /bin/false -u 47 vsftpd
  fi
  if ! getent passwd ftp >/dev/null; then
      useradd -c anonymous_user -d /home/ftp -g ftp    -s /bin/false -u 45 ftp
  fi
fi

%postun
if [ $1 -eq 0 ] ; then
  if getent passwd vsftpd >/dev/null; then
      userdel vsftpd
  fi
  if getent passwd ftp >/dev/null; then
      userdel ftp
  fi
  if getent group vsftpd >/dev/null; then
      groupdel vsftpd
  fi
fi

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_datadir}/*
%exclude %{_libdir}/debug
%changelog
*   Thu Mar 15 2018 Xiaolin Li <xiaolinl@vmware.com> 3.0.3-2
-   Enable ssl support.
*   Wed Nov 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.0.3-1
-   Upgraded to version 3.0.3, fixes CVE-2015-1419
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.2-3
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.2-2
-   Fix for upgrade issues
*   Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 3.0.2-1
-   initial version
