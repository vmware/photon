Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        14.17.6
Release:        1%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.gz
%define         sha1 node=6f1730e69ab8e87145b6ca17fa2ff73e28c52d79

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
%doc CHANGELOG.md LICENSE README.md

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/node/lldb_commands.py
%{_docdir}/node/gdbinit
%{_datadir}/systemtap/tapset/node.stp

%changelog
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
