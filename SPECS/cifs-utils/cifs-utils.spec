Summary:	cifs client utils
Name:		cifs-utils
Version:	6.4
Release:	2%{?dist}
License:	GPLv3
URL:		http://wiki.samba.org/index.php/LinuxCIFS_utils
Group:		Applications/Nfs-utils-client
Source0:    https://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-6.4.tar.bz2
%define sha1 cifs-utils=aa7067fe7b68aaa9725d368725c5c1cf081d5364
Vendor:		VMware, Inc.
Distribution:	Photon
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
%build
./configure --prefix=%{_prefix}

make
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
/sbin/mount.cifs
%{_mandir}/man8/mount.cifs.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.4-2
-	GA - Bump release of all rpms
*	Mon Jan 25 2016 Divya Thaluru <dthaluru@vmware.com> 6.4-1
-	Initial build.	First version
