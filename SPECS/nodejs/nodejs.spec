Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        10.22.1
Release:        1%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.xz
%define         sha1 node=7a684e402412ab8f9b40f936ca5665bdc9c21978
BuildRequires:  coreutils >= 8.22, zlib
Requires:       (coreutils >= 8.22 or toybox)
# To fix upgrade from photon-1.0 to photon-2.0
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
%setup -q -n node-v%{version}

%build
sh configure --prefix=%{_prefix}

make %{?_smp_mflags}

%install

make install DESTDIR=$RPM_BUILD_ROOT
rm -fr %{buildroot}%{_libdir}/dtrace/  # No systemtap support.
install -m 755 -d %{buildroot}%{_libdir}/node_modules/
install -m 755 -d %{buildroot}%{_datadir}/%{name}

# Remove junk files from node_modules/ - we should probably take care of
# this in the installer.
for FILE in .gitmodules .gitignore .npmignore .travis.yml \*.py[co]; do
  find %{buildroot}%{_libdir}/node_modules/ -name "$FILE" -delete
done

%check
make cctest

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
%{_docdir}/node/lldbinit
%{_docdir}/node/gdbinit
%{_datadir}/systemtap/tapset/node.stp

%changelog
*   Wed Oct 07 2020 Piyush Gupta <gpiyush@vmware.com> 10.22.1-1
-   Update to 10.22.1 for CVE-2020-8252
*   Mon Aug 31 2020 Piyush Gupta <gpiyush@vmware.com> 10.21.0-1
-   Update to 10.21.0
*   Fri Jul 31 2020 Ankit Jain <ankitja@vmware.com> 10.19.0-2
-   Fix for CVE-2020-8174
*   Tue Jun 09 2020 Tapas Kundu <tkundu@vmware.com> 10.19.0-1
-   Update to 10.19.0
*   Thu May 07 2020 Ankit Jain <ankitja@vmware.com> 10.15.2-2
-   To fix upgrade from 1.0 to 2.0, obsoletes nodejs10
*   Thu Apr 25 2019 Ankit Jain <ankitja@vmware.com> 10.15.2-1
-   Updated to 10.15.2
*   Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 8.11.4-1
-   Updated to version 8.11.4 to fix CVE-2018-7161 and CVE-2018-7167.
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
