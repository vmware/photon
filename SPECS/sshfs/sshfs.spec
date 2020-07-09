Summary:	fuse filesystem to access remote ssh servers
Name:           sshfs
Version:        3.7.0
Release:        1%{?dist}
License:        GPLv2
Url:		https://github.com/libfuse/sshfs
Group:		Filesystemd tools
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://github.com/libfuse/sshfs/archive/%{name}-%{version}.tar.gz
Requires:	fuse >= 2.3
Requires:	fuse3 >= 3.0.0
Requires:	glib > 2.0
Requires:       meson
BuildRequires:  fuse3-devel >= 3.0.0
BuildRequires:  meson >= 0.38.0

%define sha1 sshfs=4efb70f498020b6169adf18aa1dd746ff15ad42a
%description
This is a usermode fuse client to mount remote filesystems through SSH File Transfer Protocol.

%prep
%setup -q -n sshfs-sshfs-%{version}
%build
mkdir build &&
cd build &&
meson --prefix=%{_prefix} .. &&
ninja

%install
cd build
DESTDIR=%{buildroot}/ ninja install

#%check
#cd build
#python3 -m pytest test/

%files
%defattr(-, root, root)
%{_bindir}/*
%{_sbindir}/*
%exclude %{_libdir}
%exclude %{_prefix}/src

%changelog
*       Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.7.0-1
-       Automatic Version Bump
*       Mon Oct 08 2018 Srinidhi Rao <srinidhir@vmware.com> 3.5.0-1
-       Updated to version 3.5.0
*       Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 2.9-1
-       Updated to version 2.9
*       Fri Nov 04 2016 Sharath George <sharathg@vmware.com> 2.8-1
-       Initial commit.

