Summary:	cifs client utils
Name:		cifs-utils
Version:	6.4
Release:	4%{?dist}
License:	GPLv3
URL:		http://wiki.samba.org/index.php/LinuxCIFS_utils
Group:		Applications/Nfs-utils-client
Source0:    https://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-6.4.tar.bz2
%define sha1 cifs-utils=aa7067fe7b68aaa9725d368725c5c1cf081d5364
Vendor:		VMware, Inc.
Distribution:	Photon

Patch0:         0001-CVE-2020-14342-mount.cifs-fix-shell-command-injectio.patch

# fix for CVE-2021-20208
Patch1:         0001-cifs-upcall-try-to-use-container-ipc-uts-net-pid-mnt-user.patch

BuildRequires:  libcap-ng-devel
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
%setup -q
%patch0 -p1
%patch1 -p1

%build
./configure --prefix=%{_prefix}

make
%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
/sbin/mount.cifs
%{_mandir}/man8/mount.cifs.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
*       Tue May 11 2021 Ajay Kaher <akaher@vmware.com> 6.4-4
-       Fix for CVE-2021-20208
*       Tue Sep 15 2020 Ajay Kaher <akaher@vmware.com> 6.4-3
-       Fix for CVE-2020-14342
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.4-2
-	GA - Bump release of all rpms
*	Mon Jan 25 2016 Divya Thaluru <dthaluru@vmware.com> 6.4-1
-	Initial build.	First version
