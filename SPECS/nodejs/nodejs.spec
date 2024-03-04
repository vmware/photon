Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        16.20.2
Release:        2%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.gz
%define         sha512 node=dff6f61c323b56e2c4b1b512c388d58009e37e55340dabc748eb8508f990f12424543dd88482a8a87838ca33a33fba8a4624b5489056457120dad5b115b737d1
Patch0:         CVE-2022-25881-http-cache-semantics-4.1.1.patch
Patch1:         CVE-2024-22019.patch
Patch2:         CVE-2024-22025.patch
Patch3:         CVE-2023-46809.patch

BuildRequires:  coreutils >= 8.22, zlib
BuildRequires:  python3
BuildRequires:  which
Requires:       (coreutils >= 8.22 or toybox)
Requires:       python3
# To fix upgrade from photon-1.0 to photon-3.0
Obsoletes:      nodejs10

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
sh configure --prefix=%{_prefix}
%make_build

%install
%make_install
rm -fr %{buildroot}%{_libdir}/dtrace/  # No systemtap support.
install -m 755 -d %{buildroot}%{_libdir}/node_modules/
install -m 755 -d %{buildroot}%{_datadir}/%{name}

# Remove junk files from node_modules/ - we should probably take care of
# this in the installer.
for FILE in .gitmodules .gitignore .npmignore .travis.yml \*.py[co]; do
  find %{buildroot}%{_libdir}/node_modules/ -name "$FILE" -delete
done

%check
make cctest %{?_smp_mflags}

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/node_modules/*
%{_mandir}/man*/*
%{_datadir}/systemtap/tapset/node.stp
%doc CHANGELOG.md LICENSE README.md

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/node/lldb_commands.py
%{_docdir}/node/gdbinit

%changelog
*   Mon Mar 04 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 16.20.2-2
-   Fix CVE-2024-22019, CVE-2024-22025 and CVE-2023-46809
*   Thu Aug 24 2023 Shivani Agarwal <shivania2@vmware.com> 16.20.2-1
-   Upgrade to 16.20.2 to CVE-2023-32006
*   Wed Jul 19 2023 Siju Maliakkal <smaliakkal@vmware.com> 16.20.1-2
-   Update http-cache-semantics dependency to 4.1.1 for CVE-2022-25881
*   Tue Jun 27 2023 Siju Maliakkal <smaliakkal@vmware.com> 16.20.1-1
-   Upgrade to 16.20.1 to fix CVE-2023-30581, CVE-2023-30585
-   CVE-2023-30588, CVE-2023-30589, CVE-2023-30590
*   Thu Jun 15 2023 Siju Maliakkal <smaliakkal@vmware.com> 16.20.0-1
-   Upgrade to latest version in Gallium
*   Mon Mar 06 2023 Shivani Agarwal <shivania2@vmware.com> 16.19.1-1
-   Upgrade nodejs version to 16.19.1 for CVE-2023-23918, CVE-2023-23919 and CVE-2023-23920
*   Tue Dec 13 2022 Shivani Agarwal <shivania2@vmware.com> 16.18.1-1
-   Upgrade to 16.18.1 for CVE-2022-43548
*   Mon Oct 10 2022 Shivani Agarwal <shivania2@vmware.com> 16.17.1-1
-   Upgrade to 16.17.1 for CVE-2022-32213
*   Sun Jul 24 2022 Piyush Gupta <gpiyush@vmware.com> 16.16.0-1
-   Upgraded to 16.16.0.
*   Tue Mar 22 2022 Piyush Gupta <gpiyush@vmware.com> 16.14.2-1
-   Upgraded to 16.14.2.
*   Tue Jan 18 2022 Piyush Gupta <gpiyush@vmware.com> 16.13.2-1
-   Upgraded to 16.13.2.
*   Thu Sep 23 2021 Ankit Jain <ankitja@vmware.com> 14.17.6-1
-   Version bump to build with openssl-1.1.1l
*   Tue Sep 07 2021 Ankit Jain <ankitja@vmware.com> 14.17.5-1
-   Updated to v14.17.5 LTS version
-   Fixes CVE-2021-22931
*   Thu Feb 25 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 13.8.0-5
-   Fix second level dependency CVE-2020-1967
*   Mon Jul 27 2020 Ankit Jain <ankitja@vmware.com> 13.8.0-4
-   Fix CVE-2020-8172
*   Thu May 07 2020 Ankit Jain <ankitja@vmware.com> 13.8.0-3
-   To fix upgrade from 1.0 to 3.0, obsoletes nodejs10
*   Fri Feb 21 2020 Tapas Kundu <tkundu@vmware.com> 13.8.0-2
-   Build with python3
*   Tue Feb 18 2020 Siju Maliakkal <smaliakkal@vmware.com> 13.8.0-1
-   Upgrade to 13.8.0
*   Mon Jan 27 2020 Prashant S Chauhan <psinghchauha@vmware.com> 13.7.0-2
-   Added python and which as build dependency
*   Fri Jan 24 2020 Ankit Jain <ankitja@vmware.com> 13.7.0-1
-   Upgraded to 13.7.0
*   Fri Jan 24 2020 Ankit Jain <ankitja@vmware.com> 10.15.3-1
-   Updated to 10.15.3
*   Thu Apr 25 2019 Ankit Jain <ankitja@vmware.com> 10.15.2-1
-   Updated to 10.15.2
*   Tue Jan 08 2019 Siju Maliakkal <smaliakkal@vmware.com> 10.14.1-1
-   Upgrade to 10.14.1 LTS
*   Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 9.11.2-1
-   Updated to version 9.11.2
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 9.9.0-1
-   Updated to version 9.9.0
*   Wed Feb 14 2018 Xiaolin Li <xiaolinl@vmware.com> 8.3.0-1
-   Updated to version 8.3.0
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 7.7.4-4
-   Remove BuildArch
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 7.7.4-3
-   Requires coreutils or toybox
*   Fri Jul 14 2017 Chang Lee <changlee@vmware.com> 7.7.4-2
-   Updated %check
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 7.7.4-1
-   Initial packaging for Photon
