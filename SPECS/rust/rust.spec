Summary:        Rust Programming Language
Name:           rust
Version:        1.58.1
Release:        3%{?dist}
License:        Apache License Version 2.0 and MIT
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/rust-lang/rust/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=4f0a92434484b8ede9d96b76dc09d0a983a00832c973942224967d09228e3f985fd9d3cb757e2b768bb6b5f0d3b848e01ef5ea5d9ca33551976ab8f1793280a2

BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  glibc
BuildRequires:  binutils
BuildRequires:  curl-devel
BuildRequires:  python3-devel
BuildRequires:  openssl-devel
BuildRequires:  libssh2-devel
BuildRequires:  zlib-devel
BuildRequires:  clang >= 12.0.0
BuildRequires:  llvm-devel >= 12.0.0
BuildRequires:  xz-devel
BuildRequires:  libxml2-devel

Requires:  glibc
Requires:  gcc
Requires:  libstdc++
Requires:  openssl
Requires:  zlib
Requires:  libgcc

%description
Rust Programming Language

%prep
%autosetup -p1

rm -rf src/llvm-project/
mkdir -p src/llvm-project/libunwind/

# Remove other unused vendored libraries
rm -rf vendor/curl-sys/curl/ \
       vendor/*jemalloc-sys*/jemalloc/ \
       vendor/libmimalloc-sys/c_src/mimalloc/ \
       vendor/libssh2-sys/libssh2/ \
       vendor/libz-sys/src/zlib/ \
       vendor/libz-sys/src/zlib-ng/ \
       vendor/lzma-sys/xz-*/ \
       vendor/openssl-src/openssl/ \
       vendor/libssh2-sys/

%build
sh ./configure \
    --prefix=%{_prefix} \
    --enable-extended \
    --tools="cargo" \
    --llvm-root=%{_prefix} \
    --disable-codegen-tests

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot}%{_libdir} -maxdepth 1 -type f -name '*.so' -exec chmod -v +x '{}' '+'

rm -rf %{buildroot}%{_docdir}/%{name}/html/.lock \
       %{buildroot}%{_docdir}/%{name}/*.old \
       %{buildroot}%{_datadir}/zsh* \
       %{buildroot}%{_docdir}

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_bindir}/rust-lldb
%{_mandir}/man1/*
%{_libdir}/lib*.so
%{_libdir}/rustlib/*
%{_libexecdir}/cargo-credential-1password
%{_bindir}/rust-gdb
%{_bindir}/rust-gdbgui
%{_bindir}/cargo
%{_sysconfdir}/bash_completion.d/cargo

%changelog
* Fri May 05 2023 Harinadh D <hdommaraju@vmware.com> 1.58.1-3
- Version bump to use libssh2 1.10.0
* Tue Nov 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.58.1-2
- Reduce build time
* Sat Jan 22 2022 Ankit Jain <ankitja@vmware.com> 1.58.1-1
- Updated to 1.58.1 to fix CVE-2022-21658
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.56.0-3
- Bump up to compile with python 3.10
* Mon Nov 08 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.56.0-2
- bump up for openssl
* Thu Oct 28 2021 Ankit Jain <ankitja@vmware.com> 1.56.0-1
- Updated to 1.56.0 and fix CVE-2021-42574
* Sat Aug 28 2021 Ankit Jain <ankitja@vmware.com> 1.54.0-1
- Updated to 1.54.0
* Mon Aug 23 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-4
- Fixes CVE-2021-29922
* Tue May 04 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-3
- Fixes CVE-2020-36323
* Wed Apr 28 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-2
- Fixes CVE-2021-28876,CVE-2021-28878,CVE-2021-28879
* Mon Apr 19 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-1
- Update to latest version to fix CVE-2021-31162
* Wed Sep 02 2020 Gerrit Photon <photon-checkins@vmware.com> 1.46.0-1
- Automatic Version Bump
* Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 1.45.2-1
- Updated to 1.45.2
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 1.34.2-3
- Build with python3
- Mass removal python2
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 1.34.2-2
- Added for ARM Build
* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.34.2-1
- Initial build. First version
