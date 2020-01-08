Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        8.11.4
Release:        3%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v8.3.0/node-v%{version}.tar.xz
%define         sha1 node=195b6e6b53d04659cd6ee6afa203ad486d6eb758
Patch0:         nodejs-CVE-2018-12116.patch
Patch1:         nodejs-CVE-2018-12121.patch
Patch2:         nodejs-CVE-2018-12122.patch
Patch3:         nodejs-CVE-2019-5737.patch

BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.1
BuildRequires:  python2
BuildRequires:  which
Requires:       (coreutils >= 8.22 or toybox)
Requires:       openssl >= 1.0.1
Requires:       python2

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
./configure --prefix=%{_prefix} \
           --shared-openssl \
           --shared-zlib

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
*   Mon Jan 06 2020 Prashant S Chauhan <psinghchauha@vmware.com> 8.11.4-3
-   Added python as build requirement
*   Fri Nov 08 2019 Ankit Jain <ankitja@vmware.com> 8.11.4-2
-   Fixed CVE-2018-12116, CVE-2018-12121, CVE-2018-12122, CVE-2019-5737
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
