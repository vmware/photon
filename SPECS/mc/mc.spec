Summary:	File manager
Name:		mc
Version:	4.8.19
Release:	1%{?dist}
License:	GPLv3+
URL:		https://www.midnight-commander.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.midnight-commander.orgtar/%{name}-%{version}.tar.xz
%define sha1 mc=850747ae43a5c81f1dd0d906dfa9e149eb19748a
Requires:	glib pcre slang
BuildRequires:	glib-devel pcre-devel slang-devel

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
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
*       Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.8.19-1
-       Update package version
*	Tue Jul 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.17-1
-	Initial build.	First version
