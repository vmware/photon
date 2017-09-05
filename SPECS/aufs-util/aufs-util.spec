Summary:        Utilities for aufs
Name:           aufs-util
Version:        20170206
Release:        2%{?dist}
License:    	GPLv2
URL:        	http://aufs.sourceforge.net/
Group:        	System Environment
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        %{name}-%{version}.tar.xz
%define sha1 aufs-util=42622faa19d85737981e12d44a8e1bf5953e4d89
Source1:        aufs4.9.tar.gz
%define sha1 aufs4.9=ebe716ce4b638a3772c7cd3161abbfe11d584906
Requires:       linux-secure

%description
These utilities are always necessary for aufs.


%prep
%setup -q
%setup -D -b 1
sed -i 's/__user//' ../aufs4-standalone-aufs4.9/include/uapi/linux/aufs_type.h
sed -i '/override LDFLAGS += -static -s/d' Makefile

%build
make CPPFLAGS="-I $PWD/../aufs4-standalone-aufs4.9/include/uapi" DESTDIR=%{buildroot}

%install
make CPPFLAGS="-I $PWD/../aufs4-standalone-aufs4.9/include/uapi" DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
/etc/*
/sbin/*
/usr/*
%exclude /usr/lib/debug

%changelog
*   Fri Jul 14 2017 Alexey Makhalov <amakhalov@vmware.com> 20170206-2
-   Remove aufs source tarballs from git repo 
*   Fri Feb 10 2017 Alexey Makhalov <amakhalov@vmware.com> 20170206-1
-   Initial build. First version

