%global ncursessubversion 20230603
%define v6_so_ver   %{version}
%define v5_so_ver   5.9

Summary:        Libraries for terminal handling of character screens
Name:           ncurses
Version:        6.4
Release:        4%{?dist}
URL:            http://invisible-island.net/ncurses
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://invisible-island.net/archives/ncurses/current/%{name}-%{version}-%{ncursessubversion}.tgz
%define sha512 %{name}=5f62eeeba3a826a9c7e447cfe673d3b1f176dd39c930ddfac2550531588dbe7c73c5cc99ef0b844629c6dcd3676d4a93b5cb78d607fee824bdccfc030bdb6541

Source1: license.txt
%include %{SOURCE1}

Requires: ncurses-libs = %{version}-%{release}
Requires: glibc

BuildRequires: gcc
BuildRequires: glibc
BuildRequires: pkg-config

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

%define check_and_symlink() \
  if ! test -f %{1}; then \
    echo "ERROR: File not found: '%{1}'" 1>&2 ; \
    exit 1; \
  fi \
  ln -sfrv %{1} %{2}

%prep
%autosetup -p1 -n %{name}-%{version}-%{ncursessubversion}

%build
if [ %{_host} != %{_build} ]; then
  # configure adds incorrect includedir -I/usr/include for cross g++.
  # In result, g++ compilation will fail and configure will not
  # detect cross g++
  sed -i '/cf_includedir/d' configure
fi

mkdir -p v5 v6

for ver in 5 6; do
pushd v${ver}
ln -sf ../configure .
%configure \
    --with-shared \
    --without-normal \
    --without-debug \
    --enable-pc-files \
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \
    --enable-widec \
    --disable-lp64 \
    --with-chtype='long' \
    --with-mmask-t='long' \
    --disable-silent-rules \
    --with-termlib=tinfo \
    --with-termlib=tinfo \
    --with-abi-version=${ver}

%make_build
popd
done

%install
%make_install install.libs %{?_smp_mflags} -C v5
%make_install install.libs %{?_smp_mflags} -C v6

find %{buildroot} -name '*.a' -delete

install -vdm 755 %{buildroot}%{_libdir}

for lib in form panel menu; do
  echo "INPUT(-l${lib}w)" > %{buildroot}%{_libdir}/lib${lib}.so
  %check_and_symlink %{buildroot}%{_libdir}/pkgconfig/${lib}w.pc %{buildroot}%{_libdir}/pkgconfig/${lib}.pc
done

echo "INPUT(-lncursesw -ltinfo)" > %{buildroot}%{_libdir}/libncurses.so
echo "INPUT(-lncursesw)" > %{buildroot}%{_libdir}/libcursesw.so

%check_and_symlink %{buildroot}%{_libdir}/libncurses.so %{buildroot}%{_libdir}/libcurses.so

install -vdm 755 %{buildroot}%{_docdir}/%{name}-%{version}

%check_and_symlink %{buildroot}%{_libdir}/libncursesw.so.%{v6_so_ver} %{buildroot}%{_libdir}/libncurses.so.6

%check_and_symlink %{buildroot}%{_libdir}/libncursesw.so.%{v5_so_ver} %{buildroot}%{_libdir}/libncurses.so.5

cp -R doc/* %{buildroot}%{_docdir}/%{name}-%{version}

%check
cd test
sh ./configure
%make_build

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
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.4-4
- Release bump for SRP compliance
* Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 6.4-3
- Bump version to generate SRP provenance file
* Mon Oct 16 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 6.4-2
- Avoid hard coded versioning
- Check for source file existence before sym link creation.
* Tue May 30 2023 Nitesh Kumar <kunitesh@vmware.com> 6.4-1
- Version upgrade to 6.4 to fix CVE-2023-29491
* Mon Oct 31 2022 Susant Sahani <ssahani@vmware.com> 6.3-1
- Update to version 6.3.
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
