Summary:	File manager
Name:		mc
Version:	4.8.21
Release:	1%{?dist}
License:	GPLv3+
URL:		https://www.midnight-commander.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.midnight-commander.orgtar/%{name}-%{version}.tar.xz
%define sha1 mc=f66fec68e6e3e284b6e8f26d96001aa47c23b2d9
Patch0:		disable-extfs-test.patch
Requires:	glib pcre slang
BuildRequires:	glib-devel
BuildRequires:  pcre-devel
BuildRequires:  slang-devel

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell

%prep
%setup -q
%patch0 -p1
%build
%configure \
	--sysconfdir=/etc
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
/etc/*
/usr/bin/*
%exclude /usr/lib
/usr/libexec/*
/usr/share/*
%exclude /usr/src

%changelog
*   Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.8.21-1
-   Update to version 4.8.21
*   Fri Aug 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.8.19-2
-   Disable extfs test
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.8.19-1
-   Update package version
*   Tue Jul 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.17-1
-   Initial build. First version
