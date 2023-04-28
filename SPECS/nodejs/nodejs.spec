Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        18.10.0
Release:        4%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node

Source0: https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.gz
%define sha512 node=30a408b8f2ae41646f2ce3018862105ee4bd7913dd3cbbe8af8fc4d70cf64ac820342db9becff42c5a2b6f71d8dc3b539f580833f975b46628ad159712a8b109

BuildRequires:  (coreutils or coreutils-selinux)
BuildRequires:  zlib-devel
BuildRequires:  python3-devel
BuildRequires:  which

Requires:       python3
Requires:       (coreutils or coreutils-selinux)

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
%autosetup -p1 -n node-%{version}

%build
%{python3} configure.py \
         --enable-lto \
         --prefix=%{_prefix} \
         --libdir=%{_libdir}

%make_build

%install
%make_install %{?_smp_mflags}
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
make %{?_smp_mflags} cctest
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
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 18.10.0-4
- Bump version as a part of zlib upgrade
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 18.10.0-3
- Fix requires
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 18.10.0-2
- Update release to compile with python 3.11
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 18.10.0-1
- Update to 18.10.0 to compile with python 3.11
* Thu Mar 18 2021 Piyush Gupta <gpiyush@vmware.com> 14.16.0-1
- Upgrade to 14.16.0
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
