Summary:        Utilities for file systems, consoles, partitions, and messages
Name:           util-linux
Version:        2.32
Release:        1%{?dist}
URL:            http://www.kernel.org/pub/linux/utils/util-linux
License:        GPLv2+
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.xz
%define sha1    util-linux=4a21387d51f73bab44230c3bf9fe5a291e761111
BuildRequires:  ncurses-devel
%if %{with_check}
BuildRequires:  ncurses-terminfo
%endif
Requires: %{name}-libs = %{version}-%{release}
Conflicts:      toybox
%description
Utilities for handling file systems, consoles, partitions,
and messages.

%package lang
Summary: Additional language files for util-linux
Group: Applications/System
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of util-linux.

%package devel
Summary: Header and library files for util-linux
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel
These are the header and library files of util-linux.

%package libs
Summary: library files for util-linux
Group: Development/Libraries
%description libs
These are library files of util-linux.

%prep
%setup -q
sed -i -e 's@etc/adjtime@var/lib/hwclock/adjtime@g' $(grep -rl '/etc/adjtime' .)
%build
./configure \
    --build=%{_build} \
    --host=%{_host} \
    --target=%{_target} \
    --disable-nologin \
    --disable-silent-rules \
    --disable-static \
    --disable-use-tty-group \
    --without-python
make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}%{_sharedstatedir}/hwclock
make DESTDIR=%{buildroot} install
chmod 644 $RPM_BUILD_ROOT/usr/share/doc/util-linux/getopt/getopt*.tcsh
find %{buildroot} -name '*.la' -delete
%find_lang %{name}

%check
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"
rm -rf %{buildroot}/lib/systemd/system

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%dir %{_sharedstatedir}/hwclock
/bin/*
/lib/libfdisk.so.*
/lib/libsmartcols.so.*
/sbin/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/doc/util-linux/getopt/*

%files libs
%defattr(-,root,root)
/lib/libblkid.so.*
/lib/libmount.so.*
/lib/libuuid.so.*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
*   Mon Apr 09 2018 Xiaolin Li <xiaolinl@vmware.com> 2.32-1
-   Update to version 2.32, fix CVE-2018-7738
*   Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 2.31.1-1
-   Upgrade to version 2.31.1.
*   Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.2-5
-   Added conflicts toybox
*   Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 2.29.2-4
-   Cleanup check
*   Mon Jul 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.29.2-3
-   Fixed rpm check errors.
*   Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.2-2
-   Added -libs subpackage to strip docker image.
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2.29.2-1
-   Updated to version 2.29.2.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.27.1-5
-   Moved man3 to devel subpackage.
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 2.27.1-4
-   Disable use tty droup
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.27.1-3
-   Modified %check
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

