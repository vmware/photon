Summary:	fuse filesystem to access remote ssh servers
Name:           sshfs
Version:        3.5.0
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
BuildRequires:  fuse3-devel >= 3.0.0
BuildRequires:  meson >= 0.38.0

%define sha1 sshfs=18263ec29d4542320e52dd5390b64ca12efe536f
%description
This is a usermode fuse client to mount remote filesystems through SSH File Transfer Protocol.

%prep
%setup -q -n sshfs-sshfs-3.5.0
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
*	Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 3.5.0-1
-	Updated to version 3.5.0
*	Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 2.9-1
-	Updated to version 2.9
*	Fri Nov 04 2016 Sharath George <sharathg@vmware.com> 2.8-1
-	Initial commit.

