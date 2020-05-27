Summary:        Utilities for aufs
Name:           aufs-util
Version:        4.14
Release:        2%{?dist}
License:    	GPLv2
URL:        	http://aufs.sourceforge.net/
Group:        	System Environment
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1 aufs-util=13cbeb905bcc4add622c5a197c998fd79fb99587
Source1:        aufs4.14.tar.gz
%define sha1 aufs4.14=824c143847fe90ef3709865693552a6bc5b8d25c
BuildArch:      x86_64
Requires:       linux-secure

%description
These utilities are always necessary for aufs.


%prep
%setup -q
%setup -D -b 1
sed -i 's/__user//' ../aufs4-standalone-aufs4.14/include/uapi/linux/aufs_type.h
sed -i '/override LDFLAGS += -static -s/d' Makefile

%build
make CPPFLAGS="-I $PWD/../aufs4-standalone-aufs4.14/include/uapi" DESTDIR=%{buildroot}

%install
make CPPFLAGS="-I $PWD/../aufs4-standalone-aufs4.14/include/uapi" DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
/etc/*
/sbin/*
/usr/*
%exclude /usr/lib/debug

%changelog
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 4.14-2
-   Adding BuildArch
*   Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 4.14-1
-   Update to version 4.14
*   Fri Jul 14 2017 Alexey Makhalov <amakhalov@vmware.com> 20170206-2
-   Remove aufs source tarballs from git repo 
*   Fri Feb 10 2017 Alexey Makhalov <amakhalov@vmware.com> 20170206-1
-   Initial build. First version

