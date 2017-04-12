Summary:	fuse filesystem to access remote ssh servers
Name:           sshfs
Version:        2.8
Release:        1%{?dist}
License:        GPLv2
Url:		https://github.com/libfuse/sshfs
Group:		Filesystemd tools
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:        https://github.com/libfuse/sshfs/releases/download/%{name}_%{version}/%{name}-%{version}.tar.gz
Requires:	fuse >= 2.3
Requires:	glib >= 2.0
BuildRequires:	glib-devel >= 2.0
BuildRequires:  fuse-devel >= 2.3
BuildRequires:  fuse >= 2.3

%define sha1 sshfs=2b792aa5b3a45e0c3fe65c44bd9da8f64a690830
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
*	Fri Apr 14 2017 Danut Moraru <dmoraru@vmware.com> 2.8-1
-	Add fuse build dependency
*	Fri Nov 04 2016 Sharath George <sharathg@vmware.com> 2.8-1
-	Initial commit.

