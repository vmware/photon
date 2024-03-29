Summary:        Rust Programming Language
Name:           rust
Version:        1.71.1
Release:        2%{?dist}
License:        Apache License Version 2.0 and MIT
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://static.rust-lang.org/dist/%{name}c-%{version}-src.tar.xz
%define sha512 %{name}c-%{version}-src=fd0e5a16bdbeb539184513583089e55f681cb772810df357b6b1464853f7022ac02edab3dd155b2262ed0047e2a25dea3808dd078dcdfce9d399384465009db4

BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  glibc
BuildRequires:  binutils
BuildRequires:  curl-devel
BuildRequires:  python3-devel
BuildRequires:  openssl-devel
BuildRequires:  libssh2-devel
BuildRequires:  zlib-devel
BuildRequires:  clang
BuildRequires:  llvm-devel
BuildRequires:  xz-devel
BuildRequires:  libxml2-devel
BuildRequires:  ncurses-devel

Requires:  glibc
Requires:  gcc
Requires:  libstdc++
Requires:  openssl
Requires:  ncurses-libs
Requires:  libgcc
Requires:  zlib

%description
Rust Programming Language

%prep
%autosetup -p1 -n %{name}c-%{version}-src

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
rm %{buildroot}%{_docdir}/%{name}/html/.lock %{buildroot}%{_docdir}/%{name}/*.old

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc CONTRIBUTING.md README.md RELEASES.md
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_bindir}/rust-lldb
%{_mandir}/man1/*
%{_libdir}/lib*.so
%{_libdir}/rustlib/*
%{_libexecdir}/cargo-credential-1password
%{_bindir}/rust-gdb
%{_bindir}/rust-gdbgui
%doc %{_docdir}/%{name}/html/*
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/COPYRIGHT
%doc %{_docdir}/%{name}/LICENSE-APACHE
%doc %{_docdir}/%{name}/LICENSE-MIT
%doc src/tools/rustfmt/{README,CHANGELOG,Configurations}.md
%doc src/tools/clippy/{README.md,CHANGELOG.md}
%exclude %{_docdir}/%{name}/html/.stamp
%{_bindir}/cargo
%{_datadir}/zsh/*
%doc %{_docdir}/%{name}/LICENSE-THIRD-PARTY
%{_sysconfdir}/bash_completion.d/cargo

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.71.1-2
- Bump version as a part of openssl upgrade
* Thu Aug 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.71.1-1
- Fix CVE-2023-38497.
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 1.64.0-7
- Bump version as a part of ncurses upgrade to v6.4
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.64.0-6
- Bump version as a part of libxml2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.64.0-5
- Bump version as a part of zlib upgrade
* Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 1.64.0-4
- version bump as part of xz upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.64.0-3
- Update release to compile with python 3.11
* Wed Nov 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.64.0-2
- Add appropriate Requires
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.64.0-1
- Upgrade to v1.64.0
* Wed Nov 10 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.55.0-2
- openssl 3.0.0 compatibility
* Mon Oct 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.55.0-1
- Upgrade to 1.54.0
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
