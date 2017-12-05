Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        8.3.0
Release:        1%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node
Source0:        https://nodejs.org/download/release/v8.3.0/node-v%{version}.tar.xz
%define         sha1 node=62969b076013b20370fd42b7441b3c7ab7ac924f
BuildArch:      x86_64

BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.1
BuildRequires:  python2
Requires:       coreutils >= 8.22, openssl >= 1.0.1

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
*   Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> 8.3.0-1
-   Updated to version 8.3.0
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 7.7.4-1
-   Initial packaging for Photon
