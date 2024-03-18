Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        18.19.1
Release:        1%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node

Source0: https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.gz
%define sha512  node=039359089d0383808ac3929b97995d23bfa02b4cd150492888942fd51d6d7d60df174dbf14d7764dae379d4251ca02b6c1702bce8b79d4f99fff23c7874469f7

BuildRequires:  (coreutils or coreutils-selinux)
BuildRequires:  zlib-devel
BuildRequires:  python3-devel
BuildRequires:  which
BuildRequires:  ninja-build

Requires:       (coreutils or coreutils-selinux)
Requires:       python3
Requires:       zlib

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine. Node.js uses an event-driven, non-blocking I/O model that makes it lightweight and efficient. The Node.js package ecosystem, npm, is the largest ecosystem of open source libraries in the world.

%package        devel
Summary:        Development files node
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    devel
The nodejs-devel package contains libraries, header files and documentation
for developing applications that use nodejs.

%prep
%autosetup -p1 -n node-v%{version}

%build
sh ./configure \
       --prefix=%{_prefix} \
       --ninja

%ifarch aarch64
# aarch64 build ends up in OOM kill with -j32
%ninja_build -C out/Release -j16
%endif

%ifarch x86_64
%ninja_build -C out/Release
%endif

%install
./tools/install.py install %{buildroot} %{_prefix}
rm -fr %{buildroot}%{_libdir}/dtrace/
install -m 755 -d %{buildroot}%{_libdir}/node_modules/
install -m 755 -d %{buildroot}%{_datadir}/%{name}

# Remove junk files from node_modules/ - we should probably take care of
# this in the installer.
for FILE in .gitmodules .gitignore .npmignore .travis.yml \*.py[co]; do
  find %{buildroot}%{_libdir}/node_modules/ -name "$FILE" -delete
done

%if 0%{?with_check}
%check
make cctest %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/node_modules/*
%{_mandir}/man*/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/node/lldb_commands.py
%{_docdir}/node/gdbinit
%{_datadir}/systemtap/tapset/node.stp

%changelog
* Tue Mar 12 2024 Anmol Jain <anmol.jain@broadcom.com> 18.19.1-1
- Fix for CVE-2024-21892, CVE-2024-22025, CVE-2024-22019 & CVE-2023-46809
* Mon Oct 30 2023 Shivani Agarwal <shivania2@vmware.com> 18.18.2-1
- Upgrade to 18.18.2 to fix CVE-2023-38552
* Thu Aug 24 2023 Shivani Agarwal <shivania2@vmware.com> 18.17.1-1
- Upgrade to 18.17.1 to CVE-2023-32006, CVE-2023-32002
* Tue Jun 27 2023 Siju Maliakkal <smaliakkal@vmware.com> 18.16.1-1
- Upgrade to 18.16.1 to fix CVE-2023-30581, CVE-2023-30585
- CVE-2023-30588, CVE-2023-30589, CVE-2023-30590
* Thu Jun 15 2023 Siju Maliakkal <smaliakkal@vmware.com> 18.16.0-1
- Upgrade to latest version in Hydrogen
* Sat Apr 29 2023 Harinadh D <hdommaraju@vmware.com> 18.12.1-2
- Fix for requires
* Tue Dec 13 2022 Shivani Agarwal <shivania2@vmware.com> 18.12.1-1
- Upgrade to 18.12.1 for  CVE-2022-43548
* Wed Oct 19 2022 Shreenidhi Shedi <sshedi@vmware.com> 18.10.0-2
- Fix aarch64 build and add postun scriptlet
- Switch to ninja build
* Mon Oct 10 2022 Shivani Agarwal <shivania2@vmware.com> 18.10.0-1
- Upgrade to 18.10.0 for  CVE-2022-32213
* Tue Aug 09 2022 Shivani Agarwal <shivania2@vmware.com> 18.6.0-1
- Update to version 18.6.0
* Tue Mar 08 2022 Piyush Gupta <gpiyush@vmware.com> 17.3.1-1
- Update to version 17.3.1, fixes CVE-2021-44531,44532,44533, CVE-2022-28421.
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 17.1.0-1
- Update to version 17.1.0, build with python 3.10
* Thu Sep 23 2021 Ankit Jain <ankitja@vmware.com> 14.17.6-1
- Version bump to build with openssl-1.1.1l
* Thu Aug 26 2021 Ankit Jain <ankitja@vmware.com> 14.17.5-1
- Update to 14.17.5
* Tue Jul 20 2021 Piyush Gupta <gpiyush@vmware.com> 14.16.0-2
- Fix for CVE-2021-22918.
* Thu Mar 18 2021 Piyush Gupta <gpiyush@vmware.com> 14.16.0-1
- Upgrade to 14.16.0
* Sun Mar 14 2021 Prashant S Chauhan <psinghchauha@vmware.com> 14.13.1-2
- Fix CVE-2020-8277,Denial of Service through DNS request
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 14.13.1-1
- Update to 14.13.1 to build with python3.9
* Mon Jul 06 2020 Tapas Kundu <tkundu@vmware.com> 14.5.0-1
- Update nodejs
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 10.15.2-2
- Build with python2
* Thu Apr 25 2019 Ankit Jain <ankitja@vmware.com> 10.15.2-1
- Updated to 10.15.2
* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 10.14.1-2
- Added BuildRequires python2, which
* Tue Jan 08 2019 Siju Maliakkal <smaliakkal@vmware.com> 10.14.1-1
- Upgrade to 10.14.1 LTS
* Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 9.11.2-1
- Updated to version 9.11.2
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 9.9.0-1
- Updated to version 9.9.0
* Wed Feb 14 2018 Xiaolin Li <xiaolinl@vmware.com> 8.3.0-1
- Updated to version 8.3.0
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 7.7.4-4
- Remove BuildArch
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 7.7.4-3
- Requires coreutils or toybox
* Fri Jul 14 2017 Chang Lee <changlee@vmware.com> 7.7.4-2
- Updated %check
* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 7.7.4-1
- Initial packaging for Photon
