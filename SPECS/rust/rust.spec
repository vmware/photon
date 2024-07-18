%define toolchain_prefix        2023-06-01
%define bootstrap_toolchain_ver 1.70.0

Summary:        Rust Programming Language
Name:           rust
Version:        1.71.1
Release:        5%{?dist}
License:        Apache License Version 2.0 and MIT
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://static.rust-lang.org/dist/%{name}c-%{version}-src.tar.xz
%define sha512 %{name}c-%{version}-src=fd0e5a16bdbeb539184513583089e55f681cb772810df357b6b1464853f7022ac02edab3dd155b2262ed0047e2a25dea3808dd078dcdfce9d399384465009db4

Source1: https://static.rust-lang.org/dist/%{toolchain_prefix}/cargo-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%define sha512 cargo-%{bootstrap_toolchain_ver}-x86_64-unknown-linux-gnu=9e7a61ff6bb5a67a0ea4138259e0289c285ef7a5b3fbcad5ddcf780d2d5ec36000a5a3757b9a182b020abf646a25de3509789cf7df0fd4236231d5b92157c4e5
%endif
%ifarch aarch64
%define sha512 cargo-%{bootstrap_toolchain_ver}-aarch64-unknown-linux-gnu=70e2078a77752e51ac8bc6affcb2f81be082791ff35ef03dd5480cad9da9654234c298d8f19b418b39984a3cf885d238fe0e16d3a7b9b71b006aebf925107475
%endif

Source2: https://static.rust-lang.org/dist/%{toolchain_prefix}/rustc-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%define sha512 rustc-%{bootstrap_toolchain_ver}-x86_64-unknown-linux-gnu=790ff039749654fa3ff2f481e5fe8012e3b5fe75d075c2210e49cd4093d3d3ddcdb6690e4d9b3012e7d6361a9629ab909723f1dee8171de1f87b6b418c99aaf9
%endif
%ifarch aarch64
%define sha512 rustc-%{bootstrap_toolchain_ver}-aarch64-unknown-linux-gnu=786baefc4e4f4bda540bba9fa6fac668b8c166336a6494f1fa4057980f1ee95e34f4105409717cc61e034f98382cf8d5b59be6304d4b85de23651a2d15ed2ce2
%endif

Source3: https://static.rust-lang.org/dist/%{toolchain_prefix}/rust-std-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%define sha512 rust-std-%{bootstrap_toolchain_ver}-x86_64-unknown-linux-gnu=81ff6c73da530a5a0397ad777de2a33f7773eb58c38ba04410a3751a744c68631b0b02840170f5507c44cb4e9d2be882860e2ce663a406333ab6c57d73596956
%endif
%ifarch aarch64
%define sha512 rust-std-%{bootstrap_toolchain_ver}-aarch64-unknown-linux-gnu=8c472c23c4911c96ceea8c67c8a29aa7c99501df09ae078d6506860f5613e96039a08684ecb488b95a941550fceafec58726ea99139542cd0e27f6e126fa1b05
%endif

BuildRequires:  cmake
BuildRequires:  glibc-devel
BuildRequires:  binutils-devel
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

# Remove other unused vendored libraries
rm -rf src/llvm-project/

mkdir -p src/llvm-project/libunwind/ \
         build/cache/%{toolchain_prefix}/

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} build/cache/%{toolchain_prefix}/

%build
sh ./configure \
    --prefix=%{_prefix} \
    --enable-extended \
    --tools="cargo" \
    --llvm-root=%{_prefix} \
    --disable-codegen-tests \
    --enable-vendor

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
* Thu Jul 18 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.71.1-5
- Do offline build using vendor provided sources
- Don't remove any vendor provided sources for the same reason
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.71.1-4
- Bump version as a part of libxml2 upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.71.1-3
- Bump version as a part of libxml2 upgrade
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
