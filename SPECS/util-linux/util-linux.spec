Summary:	Utilities for file systems, consoles, partitions, and messages
Name:		util-linux
Version:	2.24.1
Release:	2%{?dist}
URL:		http://www.kernel.org/pub/linux/utils/util-linux
License:	GPLv2+
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	%{name}-%{version}.tar.xz
%define sha1 util-linux=ecf75bbb77bba874fc11fc27423aa67b395b7ae5
BuildRequires:	ncurses-devel
%description
Utilities for handling file systems, consoles, partitions,
and messages.

%package lang
Summary: Additional language files for util-linux
Group: Applications/System
Requires: util-linux >= 2.24.1
%description lang
These are the additional language files of util-linux.

%prep
%setup -q
sed -i -e 's@etc/adjtime@var/lib/hwclock/adjtime@g' $(grep -rl '/etc/adjtime' .)
%build
./configure \
	--disable-nologin \
	--disable-silent-rules
make %{?_smp_mflags}
%install
install -vdm 755 %{buildroot}%{_sharedstatedir}/hwclock
make DESTDIR=%{buildroot} install
chmod 644 $RPM_BUILD_ROOT/usr/share/doc/util-linux/getopt/getopt*.tcsh
find %{buildroot} -name '*.la' -delete
%find_lang %{name}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%dir %{_sharedstatedir}/hwclock
/bin/*
/lib/*.so.*
/sbin/*
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_sbindir}/*
%{_mandir}/*/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/doc/util-linux/getopt/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 2.24.1-2
-   Update according to UsrMove.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.24.1-1
-	Initial build. First version

