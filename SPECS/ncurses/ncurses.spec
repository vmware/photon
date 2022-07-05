%global ncursessubversion 20210807

Summary:        Libraries for terminal handling of character screens
Name:           ncurses
Version:        6.2
Release:        5%{?dist}
License:        MIT
URL:            http://invisible-island.net/ncurses
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.invisible-island.net/ncurses/current/%{name}-%{version}-%{ncursessubversion}.tgz
%define sha1    %{name}=4e1221ea1cc96ee41466c24199931f4d044467c6

Requires:       ncurses-libs = %{version}-%{release}
Requires:       glibc

BuildRequires:  gcc glibc
BuildRequires:  pkg-config

%description
The Ncurses package contains libraries for terminal-independent
handling of character screens.

%package        libs
Summary:        Ncurses Libraries
Group:          System Environment/Libraries
Provides:       libncurses.so.6()(64bit)

%description    libs
This package contains ncurses libraries

%package        compat
Summary:        Ncurses compatibility libraries
Group:          System Environment/Libraries
Provides:       libncurses.so.5()(64bit)

%description    compat
This package contains the ABI version 5 of the ncurses libraries for
compatibility.

%package        devel
Summary:        Header and development files for ncurses
Requires:       %{name} = %{version}-%{release}
Provides:       pkgconfig(ncurses)

%description    devel
It contains the libraries and header files to create applications

%package        terminfo
Summary:        terminfo files for ncurses
Requires:       %{name} = %{version}-%{release}

%description    terminfo
It contains all terminfo files

%prep
%autosetup -p1 -n %{name}-%{version}-%{ncursessubversion}

%build
if [ %{_host} != %{_build} ]; then
    # configure adds incorrect includedir -I/usr/include for cross g++.
    # In result, g++ compilation will fail and configure will not
    # detect cross g++
    sed -i '/cf_includedir/d' configure
fi

mkdir v6
pushd v6
ln -s ../configure .
%configure \
    --with-shared \
    --without-debug \
    --enable-pc-files \
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \
    --enable-widec \
    --disable-lp64 \
    --with-chtype='long' \
    --with-mmask-t='long' \
    --disable-silent-rules \
    --with-termlib=tinfo
make %{?_smp_mflags}
popd

mkdir v5
pushd v5
ln -s ../configure .
%configure \
    --with-shared \
    --without-debug \
    --enable-pc-files \
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \
    --enable-widec \
    --disable-lp64 \
    --with-chtype='long' \
    --with-mmask-t='long' \
    --disable-silent-rules \
    --with-termlib=tinfo \
    --with-abi-version=5
make %{?_smp_mflags}
popd

%install
make %{?_smp_mflags} -C v5 DESTDIR=%{buildroot} install.libs
make %{?_smp_mflags} -C v6 DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_lib}
ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_libdir}/libncursesw.so) %{buildroot}%{_libdir}/libncursesw.so

for lib in form panel menu; do
    rm -vf %{buildroot}%{_libdir}/lib${lib}.so
    echo "INPUT(-l${lib}w)" > %{buildroot}%{_libdir}/lib${lib}.so
    ln -sfv lib${lib}w.a %{buildroot}%{_libdir}/lib${lib}.a
    ln -sfv %{_libdir}/pkgconfig/${lib}w.pc %{buildroot}%{_libdir}/pkgconfig/${lib}.pc
done

for lib in ncurses; do
    rm -vf %{buildroot}%{_libdir}/lib${lib}.so
    echo "INPUT(-l${lib}w -ltinfo)" > %{buildroot}%{_libdir}/lib${lib}.so
    ln -sfv lib${lib}w.a %{buildroot}%{_libdir}/lib${lib}.a
done

ln -sfv libncurses++w.a %{buildroot}%{_libdir}/libncurses++.a
rm -vf %{buildroot}%{_libdir}/libcursesw.so
echo "INPUT(-lncursesw)" > %{buildroot}%{_libdir}/libcursesw.so
ln -sfv libncurses.so %{buildroot}%{_libdir}/libcurses.so
ln -sfv libncursesw.a %{buildroot}%{_libdir}/libcursesw.a
ln -sfv libncurses.a %{buildroot}%{_libdir}/libcurses.a
install -vdm 755  %{buildroot}%{_defaultdocdir}/%{name}-%{version}
ln -sv libncursesw.so.6.2 %{buildroot}%{_libdir}/libncurses.so.6
ln -sv libncursesw.so.5.9 %{buildroot}%{_libdir}/libncurses.so.5
cp -v -R doc/* %{buildroot}%{_defaultdocdir}/%{name}-%{version}

%check
%if 0%{?with_check}
cd test
sh configure
make %{?_smp_mflags}
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post compat -p /sbin/ldconfig
%postun compat -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/captoinfo
%{_bindir}/clear
%{_bindir}/tabs
%{_bindir}/tic
%{_bindir}/tset
%{_bindir}/reset
%{_bindir}/infocmp
%{_bindir}/tput
%{_bindir}/infotocap
%{_bindir}/toe
%{_mandir}/man7/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files libs
%{_datadir}/terminfo/l/linux
%{_datadir}/tabset/*
%{_libdir}/terminfo
%{_libdir}/lib*.so.6*

%files compat
%{_libdir}/lib*.so.5*
%{_bindir}/ncursesw5-config

%files devel
%{_bindir}/ncursesw6-config
%{_includedir}/*.h
%{_libdir}/libncurses.a
%{_libdir}/libformw.a
%{_libdir}/libpanel.a
%{_libdir}/libmenuw.a
%{_libdir}/libncursesw.a
%{_libdir}/libcursesw.a
%{_libdir}/libncurses++w.a
%{_libdir}/libform.a
%{_libdir}/libcurses.a
%{_libdir}/libpanelw.a
%{_libdir}/libncurses++.a
%{_libdir}/libmenu.a
%{_libdir}/libtinfo.a
%{_libdir}/libpanelw.so
%{_libdir}/libcurses.so
%{_libdir}/libformw.so
%{_libdir}/libmenuw.so
%{_libdir}/libncurses.so
%{_libdir}/libform.so
%{_libdir}/libcursesw.so
%{_libdir}/libpanel.so
%{_libdir}/libmenu.so
%{_libdir}/libtinfo.so
%{_libdir}/pkgconfig/formw.pc
%{_libdir}/pkgconfig/menuw.pc
%{_libdir}/pkgconfig/form.pc
%{_libdir}/pkgconfig/menu.pc
%{_libdir}/pkgconfig/panel.pc
%{_libdir}/pkgconfig/ncurses++w.pc
%{_libdir}/pkgconfig/ncursesw.pc
%{_libdir}/pkgconfig/panelw.pc
%{_libdir}/pkgconfig/tinfo.pc
%{_libdir}/libncursesw.so

%{_docdir}/ncurses-%{version}/html/*
%{_docdir}/ncurses-%{version}/*.doc
%{_mandir}/man3/*

%files terminfo
%defattr(-,root,root)
%{_datadir}/terminfo/*
%exclude %{_datadir}/terminfo/l/linux

%changelog
* Mon Mar 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 6.2-5
- Add symlinks to keep libraries backward compatible
* Thu Nov 18 2021 Oliver Kurth <okurth@vmware.com> 6.2-4
- update to 20210807
- add libtinfo
- use smp_mflags and autosetup
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 6.2-3
- Fix build with new rpm
* Fri Aug 28 2020 Gerrit Photon <photon-checkins@vmware.com> 6.2-2
- Automatic Version Bump
* Thu Aug 13 2020 Susant Sahani <ssahani@vmware.com> 6.2-1
- Update to version 6.2.
* Wed Nov 07 2018 Alexey Makhalov <amakhalov@vmware.com> 6.1-2
- Cross compilation support
* Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.1-1
- Update to version 6.1.
* Tue Jul 17 2018 Tapas Kundu <tkundu@vmware.com> 6.0-14
- Fix for CVE-2018-10754
* Wed Dec 06 2017 Xiaolin Li <xiaolinl@vmware.com> 6.0-13
- version bump to 20171007, fix CVE-2017-16879
* Tue Oct 10 2017 Bo Gan <ganb@vmware.com> 6.0-12
- version bump to 20171007
- Fix for CVE-2017-11112, CVE-2017-11113 and CVE-2017-13728
* Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> 6.0-11
- ncurses-devel provides pkgconfig(ncurses)
* Thu Aug 10 2017 Bo Gan <ganb@vmware.com> 6.0-10
- Move ncursesw6-config to devel
* Thu Jul 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 6.0-9
- Fix for CVE-2017-10684 and CVE-2017-10685
* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> 6.0-8
- Fix bash dependency
* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 6.0-7
- Fix symlink
* Wed Mar 29 2017 Alexey Makhalov <amakhalov@vmware.com> 6.0-6
- --with-chtype=long --with-mmask-t=long to avoid type clashes (1838226)
* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 6.0-5
- Add -terminfo subpackage. Main package carries only 'linux' terminfo
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 6.0-4
- Move doc and man3 to the devel package
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 6.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-2
- GA - Bump release of all rpms
* Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 6.0-1
- Update to version 6.0.
* Wed Nov 18 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 5.9-4
- Package provides libncurses.so.5()(64bit)
* Tue Nov 10 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 5.9-3
- Add libncurses.so.5, and minor fix in the devel package
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 5.9-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.9-1
- Initial build. First version
