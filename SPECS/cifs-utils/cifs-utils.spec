Summary:	cifs client utils
Name:		cifs-utils
Version:	6.8
Release:	4%{?dist}
License:	GPLv3
URL:		http://wiki.samba.org/index.php/LinuxCIFS_utils
Group:		Applications/Nfs-utils-client
Source0:        https://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-%{version}.tar.bz2
%define sha512 cifs-utils=54a094f78c9e07acc997adfe0c8d4c2fb8e15c18adcc1805450e2180f8539aaec8619e781e985b289e097932637e2de3e6815e32f59ec2fc06cfc3762b832e13
Vendor:		VMware, Inc.
Distribution:	Photon

Patch0:         0001-CVE-2020-14342-mount.cifs-fix-shell-command-injectio.patch

# fix for CVE-2021-20208
Patch1:         0001-cifs-upcall-try-to-use-container-ipc-uts-net-pid-mnt-user.patch

# fix for CVE-2022-27239
Patch2:         0001-CVE-2022-27239_mount_cifs_fix_length_check_for_ip_option_parsing.patch

# fix for CVE-2022-29869
Patch3:         0001-mount.cifs_fix_verbose_messages_on_option_parsing.patch

BuildRequires:  libcap-ng-devel
BuildRequires:  libtalloc-devel
Requires:       libcap-ng

%description
Cifs-utils, a package of utilities for doing and managing mounts of the Linux CIFS filesystem.

%package devel
Summary:    The libraries and header files needed for Cifs-Utils development.
Group:      Development/Libraries
Requires:   cifs-utils = %{version}-%{release}

%description devel
Provides header files needed for Cifs-Utils development.

%prep
%autosetup -p1

%build
autoreconf -fiv &&./configure --prefix=%{_prefix}
make

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
/sbin/mount.cifs

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
*       Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 6.8-4
-       Fix for CVE-2022-27239, CVE-2022-29869
*       Tue May 11 2021 Ajay Kaher <akaher@vmware.com> 6.8-3
-       Fix for CVE-2021-20208
*       Tue Sep 15 2020 Ajay Kaher <akaher@vmware.com> 6.8-2
-       Fix for CVE-2020-14342
*       Thu Sep 07 2017 Ajay Kaher <akaher@vmware.com> 6.8-1
-       Upgraded to version 6.8
*       Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 6.7-1
-       Upgraded to version 6.7
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.4-2
-	GA - Bump release of all rpms
*	Mon Jan 25 2016 Divya Thaluru <dthaluru@vmware.com> 6.4-1
-	Initial build.	First version
