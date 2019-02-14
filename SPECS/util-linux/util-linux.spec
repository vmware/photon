Summary:	Utilities for file systems, consoles, partitions, and messages
Name:		util-linux
Version:	2.27.1
Release:	4%{?dist}
URL:		http://www.kernel.org/pub/linux/utils/util-linux
License:	GPLv2+
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	%{name}-%{version}.tar.xz
%define sha1 util-linux=462bca6320535d39b62216d8609da5531bfef0bb
Patch0:         CVE-2017-2616.patch
BuildRequires:	ncurses-devel >= 6.0-3
Requires:	ncurses >= 6.0-3
%description
Utilities for handling file systems, consoles, partitions,
and messages.

%package lang
Summary: Additional language files for util-linux
Group: Applications/System
Requires: util-linux >= 2.24.1
%description lang
These are the additional language files of util-linux.

%package devel
Summary: Header and library files for util-linux
Group: Development/Libraries
Requires: util-linux >= 2.24.1
%description devel
These are the header and library files of util-linux.

%prep
%setup -q
%patch0 -p1
sed -i -e 's@etc/adjtime@var/lib/hwclock/adjtime@g' $(grep -rl '/etc/adjtime' .)
%build
./configure \
	--disable-nologin \
	--disable-silent-rules \
	--disable-static \
	--without-python
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
%{_sbindir}/*
%{_mandir}/*/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/doc/util-linux/getopt/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/*

%changelog
*   Thu Feb 14 2019 Keerthana K <keerthanak@vmware.com> 2.27.1-4
-   Fix for CVE-2017-2616.
*   Mon Apr 3 2017 Alexey Makhalov <amakhalov@vmware.com> 2.27.1-3
-   Use specified version of ncurses wich has long chtype and mmask_t
    (see ncurses changelog)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.27.1-2
-   GA - Bump release of all rpms
*   Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 2.27.1-1
-   Upgrade version.
*   Tue Oct 6 2015 Xiaolin Li <xiaolinl@vmware.com> 2.24.1-3
-   Disable static, move header files, .so and config files to devel package.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 2.24.1-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.24.1-1
-   Initial build. First version

