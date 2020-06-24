Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        8.11.4
Release:        5%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v8.3.0/node-v%{version}.tar.xz
%define         sha1 node=195b6e6b53d04659cd6ee6afa203ad486d6eb758
BuildArch:      x86_64
Patch0:         nodejs-CVE-2018-12116.patch
Patch1:         nodejs-CVE-2018-12121.patch
Patch2:         nodejs-CVE-2018-12122.patch
Patch3:         nodejs-CVE-2019-5737.patch
Patch4:		CVE-2018-0734.patch
Patch5:		nodejs-CVE-2018-12123.patch

BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.1
BuildRequires:  python2
Requires:       coreutils >= 8.22, openssl >= 1.0.1
# Kibana Requires nodejs10
# kubernetes-dashboard Requires nodejs-8
# Only one of the nodejs version can exist in system
# Thus obsoleting nodejs10 if nodejs-8 need to be installed
# And in nodejs10.spec, obsoleting nodejs-8 if nodejs10 need to be installed
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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
make  %{?_smp_mflags} test

%post
    /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/node_modules/*
%{_mandir}/man*/*
%doc CHANGELOG.md LICENSE README.md

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/node/gdbinit
%{_docdir}/node/lldb_commands.py
%{_docdir}/node/lldbinit
%{_datadir}/systemtap/tapset/node.stp

%changelog
*   Tue Jun 16 2020 Siju Maliakkal <smaliakkal@vmware.com> 8.11.4-5
-   Fix for CVE-2018-12123
*   Mon Jun 01 2020 Siju Maliakkal <smaliakkal@vmware.com> 8.11.4-4
-   Fix for CVE-2018-0734
*   Fri Nov 08 2019 Ankit Jain <ankitja@vmware.com> 8.11.4-3
-   Fixed CVE-2018-12116, CVE-2018-12121, CVE-2018-12122, CVE-2019-5737
*   Tue Apr 16 2019 Ankit Jain <ankitja@vmware.com> 8.11.4-2
-   Added obsoletes to downgrade nodejs10 to nodejs8
*   Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 8.11.4-1
-   Updated to version 8.11.4 to fix CVE-2018-7161 and CVE-2018-7167
*   Mon Jul 16 2018 Keerthana K <keerthanak@vmware.com> 8.11.0-1
-   Updated to version 8.11.0
*   Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> 8.3.0-1
-   Updated to version 8.3.0
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 7.7.4-1
-   Initial packaging for Photon
