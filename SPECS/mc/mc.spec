Summary:	File manager
Name:		mc
Version:	4.8.19
Release:	2%{?dist}
License:	GPLv3+
URL:		https://www.midnight-commander.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.midnight-commander.orgtar/%{name}-%{version}.tar.xz
%define sha1 mc=850747ae43a5c81f1dd0d906dfa9e149eb19748a
Source1:	hp48+.output
Source2:	rpm.custom.output
Source3:	rpm.glib.output
Source4:	uace.output
Source5:	uarc.output
Source6:	uzoo.output
Source7:	u7z.complex.output
Source8:	u7z.missing-size-and-date.output
Source9:	u7z.simple.output
Source10:	urar.v4,v3.output
Source11:	urar.v5.output
Requires:	glib pcre slang
BuildRequires:	glib-devel pcre-devel slang-devel

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell

%prep
%setup -q
cp %{SOURCE1} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE2} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE3} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE4} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE5} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE6} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE7} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE8} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE9} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE10} tests/src/vfs/extfs/helpers-list/data/
cp %{SOURCE11} tests/src/vfs/extfs/helpers-list/data/

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
*       Mon Aug 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.8.19-2
-       Fix makecheck issues
*       Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.8.19-1
-       Update package version
*	Tue Jul 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.17-1
-	Initial build.	First version
