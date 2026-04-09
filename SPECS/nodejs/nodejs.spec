Summary:        A JavaScript runtime built on Chrome's V8 JavaScript engine.
Name:           nodejs
Version:        22.22.2
Release:        1%{?dist}
License:        MIT
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/nodejs/node

Source0: https://nodejs.org/download/release/v%{version}/node-v%{version}.tar.gz
%define sha512  node=7595b55a7bb96320d4f4289fad3a289b04e2ad6ca47643aa6de9247c1d7020e7e79d03a54b46eed30989f301541afdbec4a6c9aa4885b06579c6c4d0dbcf318e

BuildRequires:  (coreutils or coreutils-selinux)
BuildRequires:  zlib-devel
BuildRequires:  python3-devel
BuildRequires:  which
BuildRequires:  openssl-devel
BuildRequires:  nghttp2-devel
BuildRequires:  ninja-build
BuildRequires:  python3-jinja2
BuildRequires:  python3-markupsafe

Requires:       python3
Requires:       (coreutils or coreutils-selinux)
Requires:       nghttp2
Requires:       openssl
Requires:       libstdc++
Requires:       libgcc
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

rm -r deps/zlib \
      deps/nghttp2

rm -r deps/v8/third_party/glibc \
       deps/v8/third_party/jsoncpp \
       deps/v8/third_party/re2 \
       deps/v8/third_party/jinja2 \
       deps/v8/third_party/markupsafe

%build
%{python3} configure.py \
  --ninja \
  --enable-lto \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --shared-nghttp2 \
  --shared-openssl \
  --shared-zlib \
  --with-intl=small-icu \
  --openssl-use-def-ca-store

# Do not use all cores to prevent resource exhaustion
build_jobs="$(( ($(nproc)+1) / 2 ))"
ninja -v -j${build_jobs} -C out/Release

%install
%make_install %{?_smp_mflags}

# Remove unneeded files from node_modules
for FILE in .gitmodules .gitignore .npmignore .travis.yml \*.py[co]; do
  find %{buildroot}%{_libdir}/node_modules/ -name "$FILE" -delete
done

%if 0%{?with_check}
%check
%make_build cctest
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

%changelog
* Thu Apr 09 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 22.22.2-1
- Fix CVE-2026-21710, CVE-2026-21714, CVE-2026-21717, CVE-2026-21715, CVE-2026-21713, CVE-2026-2171
* Mon Feb 02 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 22.22.0-1
- Upgrade to 22.22.0 to fix multiple CVE's
* Thu Jan 08 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 22.17.1-2
- Use ninja for building
- Use system provided packages for building
* Tue Jul 22 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 22.17.1-1
- Upgrade to 22.17.1 to fix CVE-2025-27210
* Tue Jul 01 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 22.16.0-2
- Fix ARM build
* Mon Jun 23 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 22.16.0-1
- Upgrade to 22.16.0 to fix CVE-2025-23167 and CVE-2025-23090
* Mon May 26 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 18.20.8-2
- Fix CVE-2025-23166
* Fri May 16 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 18.20.8-1
- Upgrade to 18.20.8
* Mon Jul 15 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 18.20.4-1
- Upgrade to 18.20.4 to fix CVE-2024-22020, CVE-2024-36138
* Wed Jun 19 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 18.20.3-1
- Upgrade to 18.20.3 to fix CVE-2024-27982, CVE-2024-27983
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
