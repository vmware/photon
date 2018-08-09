Summary:	Lynx is a text browser for the World Wide Web
Name:           lynx
Version:        2.8.9rel.1
Release:        1%{?dist}
License:        GPLv2
Group:          Productivity/Networking/Other
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://lynx.invisible-island.net
Source:         https://invisible-mirror.net/archives/lynx/tarballs/%{name}%{version}.tar.gz
%define sha1 %{name}%{version}=a76e6320f2ee00275ba035f29d6b3f9fef6c1f69
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel

%description
Lynx is a fully-featured World Wide Web (WWW) client for users running
cursor-addressable, character-cell display devices such as vt100 terminals,
vt100 emulators running on Windows 95/NT or Macintoshes, or any other
character-cell display.  It will display Hypertext Markup Language (HTML)
documents containing links to files on the local system, as well as files on
remote systems running http, gopher, ftp, wais, nntp, finger, or cso/ph/qi
servers, and services accessible via logins to telnet, tn3270 or rlogin
accounts.  Current versions of Lynx run on Unix, VMS, Windows95
through Windows 8, 386DOS and OS/2 EMX.

%prep
%setup -q -n %{name}%{version}

%build
%configure \
	--enable-debug \
	--enable-nls \
	--with-ssl
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
chmod ogu-x scripts/conf.mingw.sh scripts/config.djgpp.sh

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%config %{_sysconfdir}/%{name}.lss
%{_datadir}/locale/*
%doc %{_mandir}/man1/%{name}.1.gz
%doc scripts samples lynx_help
%doc AUTHORS CHANGES README COPYING README PROBLEMS

%changelog
*   Thu Aug 09 2018 Ankit Jain <ankitja@vmware.com> 2.8.9rel.1-1
-   Initial Version.
