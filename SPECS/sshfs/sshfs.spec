Summary:	fuse filesystem to access remote ssh servers
Name:           sshfs
Version:        2.9
Release:        1%{?dist}
License:        GPLv2
URL:		https://github.com/libfuse/sshfs
Group:		Filesystemd tools
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://github.com/libfuse/sshfs/releases/download/%{name}_%{version}/%{name}-%{version}.tar.gz
Requires:	fuse >= 2.3
Requires:	glib >= 2.0
BuildRequires:	glib-devel >= 2.0
BuildRequires:  fuse-devel >= 2.3
%define sha1 sshfs=57d2d600c0cdf7cb48a8cd0dbcdcfd99309fb04b
%description
This is a usermode fuse client to mount remote filesystems through SSH File Transfer Protocol.

%prep
%setup -q
%build
autoreconf -i
./configure --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make install prefix=%{buildroot}%{_prefix}

%files
%defattr(-, root, root)
%{_bindir}/*
%{_datadir}/man/*


%changelog
*	Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 2.9-1
-	Updated to version 2.9
*	Fri Nov 04 2016 Sharath George <sharathg@vmware.com> 2.8-1
-	Initial commit.

