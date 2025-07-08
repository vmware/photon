%define toolchain_prefix        2021-12-02
%define bootstrap_toolchain_ver 1.57.0

Summary:        Rust Programming Language
Name:           rust
Version:        1.58.1
Release:        6%{?dist}
License:        Apache License Version 2.0 and MIT
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://static.rust-lang.org/dist/%{name}c-%{version}-src.tar.xz
%define sha512 %{name}c-%{version}-src=eff3279d2e519343cea542a9ae2daab592e44f35af344e33ff43ed55fc7c824511790d1991dd36a603d12465de8c3688e7194c2b9557f288c587ffa04738c2ce

Source1: https://static.rust-lang.org/dist/%{toolchain_prefix}/cargo-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%define sha512 cargo-%{bootstrap_toolchain_ver}-x86_64-unknown-linux-gnu=ca84cfc9f0d52443aa41da1e18fe013d1c0412882e061b391d80b6a2fcc3c6858c923ee2dd53174c60c845fbd26523b62a9e1279b888bdc3c409702754d94557
%endif
%ifarch aarch64
%define sha512 cargo-%{bootstrap_toolchain_ver}-aarch64-unknown-linux-gnu=f99ac5d4ad6c8abb30116cb88f7eb6bd7e2e681f71b4a0345af992d32fa78b2acbd130bc41c581539153ebb9908f24e81dbfa12d8eca9c31e01ef1f3d1e6cf37
%endif

Source2: https://static.rust-lang.org/dist/%{toolchain_prefix}/rustc-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%define sha512 rustc-%{bootstrap_toolchain_ver}-x86_64-unknown-linux-gnu=dca0cf813d42bec4f0b5395c7bc1e0f0049d987247120dcbc87b5234ae32178e1b95b5ae955ec99125ab9e88e8c60d2665becd971c43b30a25ef2c63fc6de1c1
%endif
%ifarch aarch64
%define sha512 rustc-%{bootstrap_toolchain_ver}-aarch64-unknown-linux-gnu=3931771ad8e352c8d412193f69d6791c38c843b9435e79237e3968cd460a9b6cdb2c1b84ed576500017bc70e81624d3c120b4a452821a588d0af5a20d298f9b4
%endif

Source3: https://static.rust-lang.org/dist/%{toolchain_prefix}/rust-std-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%define sha512 rust-std-%{bootstrap_toolchain_ver}-x86_64-unknown-linux-gnu=1257ab3648d6569c827096253b60075b32ac3529e42fc68220cd0b83cecc2fda1a8187c716f81556069cd931d4a79cc4f8b7f7ea89cb8f0d1f244b41f0d4a15c
%endif
%ifarch aarch64
%define sha512 rust-std-%{bootstrap_toolchain_ver}-aarch64-unknown-linux-gnu=3977195413b1272f1364defadc444ccf6152410e4f926f6617052648e79bf9888df0a8a2415a75c224ef79a52c801ed91952017bf6659aa0d41a8cc59c9251a4
%endif

Patch0:         0001-fix-respect-umask-when-unpacking-.crate-files.patch
Patch1:         0002-fix-clear-cache-for-old-.cargo-ok-format.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  glibc-devel
BuildRequires:  binutils-devel
BuildRequires:  curl-devel
BuildRequires:  python3-devel
BuildRequires:  openssl-devel
BuildRequires:  libssh2-devel
BuildRequires:  zlib-devel
BuildRequires:  clang >= 12.0.0
BuildRequires:  llvm-devel >= 12.0.0
BuildRequires:  xz-devel
BuildRequires:  libxml2-devel

Requires:  glibc-devel
Requires:  gcc
Requires:  libstdc++
Requires:  openssl
Requires:  zlib
Requires:  libgcc
Requires:  binutils

%description
Rust Programming Language

%prep
%autosetup -p1 -n %{name}c-%{version}-src

rm -rf src/llvm-project/

# Remove other unused vendored libraries
rm -rf vendor/curl-sys/curl/ \
       vendor/*jemalloc-sys*/jemalloc/ \
       vendor/libmimalloc-sys/c_src/mimalloc/ \
       vendor/libz-sys/src/zlib/ \
       vendor/libz-sys/src/zlib-ng/ \
       vendor/lzma-sys/xz-*/ \
       vendor/openssl-src/openssl/ \
       vendor/libssh2-sys/

mkdir -p build/cache/%{toolchain_prefix}/
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} build/cache/%{toolchain_prefix}/

%build
sh ./configure \
    --prefix=%{_prefix} \
    --enable-extended \
    --tools="cargo" \
    --llvm-root=%{_prefix} \
    --disable-codegen-tests \
    --enable-ninja

# Output sync option (-O) in make results in buffered logging.
# For a long time we don't say any logs during build, hence disabling it
%define _make_output_sync %{nil}
%make_build BOOTSTRAP_ARGS=-vv

%install
%make_install %{?_smp_mflags}
find %{buildroot}%{_libdir} -maxdepth 1 -type f -name '*.so' -exec chmod -v +x '{}' '+'

rm -rf %{buildroot}%{_docdir} \
       %{buildroot}%{_datadir}/zsh*

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
* Thu Jul 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.58.1-6
- Enable verbose build
* Wed Aug 30 2023 Harinadh D <hdommaraju@vmware.com> 1.58.1-5
- Version bump to use libssh2 1.11.0
* Fri Aug 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.58.1-4
- Fix CVE-2023-38497.
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
