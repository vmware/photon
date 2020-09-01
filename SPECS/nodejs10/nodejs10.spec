Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs10
Version:        10.21.0
Release:        1%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.xz
%define         sha1 node=0c2e544d330e82b01952e9a17d79d48f8f106c50
BuildArch:      x86_64
BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.1
BuildRequires:  python2
Requires:       coreutils >= 8.22, openssl >= 1.0.1
# Kibana Requires nodejs10
# kubernetes-dashboard Requires nodejs-8
# Only one of the nodejs version can exist in system
# Thus obsoleting nodejs if nodejs10 need to be installed
# And in nodejs.spec, obsoleting nodejs10 if nodejs-8 need to be installed
Obsoletes:      nodejs <= 8.11.4

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
./configure --prefix=%{_prefix}

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
*   Mon Aug 31 2020 Piyush Gupta <gpiyush@vmware.com> 10.21.0-1
-   Update to version 10.21.0
*   Fri Jul 31 2020 Ankit Jain <ankitja@vmware.com> 10.19.0-3
-   Fix for CVE-2020-8174
*   Thu May 07 2020 Ankit Jain <ankitja@vmware.com> 10.19.0-2
-   Obsoletes specific version of nodejs
*   Thu Apr 09 2020 Siju Maliakkal <smaliakkal@vmware.com> 10.19.0-1
-   Upgrade to 10.19.0 for CVE-2019-15604,CVE-2019-15605,CVE-2019-15606
*   Thu Jan 30 2020 Siju Maliakkal <smaliakkal@vmware.com> 10.18.0-1
-   Upgrade to use higher openssl version
*   Tue Apr 02 2019 Ankit Jain <ankitja@vmware.com> 10.15.2-1
-   Initial Version
