%define toolchain_prefix        2023-06-01
%define bootstrap_toolchain_ver 1.70.0

Summary:        Rust Programming Language
Name:           rust
Version:        1.71.1
Release:        5%{?dist}
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://static.rust-lang.org/dist/%{name}c-%{version}-src.tar.xz

Source1: https://static.rust-lang.org/dist/%{toolchain_prefix}/cargo-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%endif
%ifarch aarch64
%endif

Source2: https://static.rust-lang.org/dist/%{toolchain_prefix}/rustc-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%endif
%ifarch aarch64
%endif

Source3: https://static.rust-lang.org/dist/%{toolchain_prefix}/rust-std-%{bootstrap_toolchain_ver}-%{_arch}-unknown-linux-gnu.tar.xz
%ifarch x86_64
%endif
%ifarch aarch64
%endif

Source4: license.txt
%include %{SOURCE4}

Patch0: 0001-Convert-valid-feature-name-warning-to-an-error.patch

BuildRequires: cmake
BuildRequires: glibc-devel
BuildRequires: binutils-devel
BuildRequires: curl-devel
BuildRequires: python3-devel
BuildRequires: openssl-devel
BuildRequires: libssh2-devel
BuildRequires: zlib-devel
BuildRequires: clang
BuildRequires: llvm-devel
BuildRequires: xz-devel
BuildRequires: libxml2-devel
BuildRequires: ncurses-devel

Requires: glibc
Requires: gcc
Requires: libstdc++
Requires: openssl
Requires: ncurses-libs
Requires: libgcc
Requires: zlib

%description
Rust Programming Language

%prep
# Using autosetup is not feasible
%setup -q -n %{name}c-%{version}-src

pushd src/tools/cargo
%autopatch -p1 -M0
popd

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
%exclude %{_docdir}/%{name}/html/.stamp
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/COPYRIGHT
%doc %{_docdir}/%{name}/LICENSE-APACHE
%doc %{_docdir}/%{name}/LICENSE-MIT
%doc src/tools/rustfmt/{README,CHANGELOG,Configurations}.md
%doc src/tools/clippy/{README.md,CHANGELOG.md}
%{_bindir}/cargo
%{_datadir}/zsh/*
%doc %{_docdir}/%{name}/LICENSE-THIRD-PARTY
%{_sysconfdir}/bash_completion.d/cargo

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.71.1-5
- Release bump for SRP compliance
* Thu Jul 18 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.71.1-4
- Do offline build using vendor provided sources
- Don't remove any vendor provided sources for the same reason
* Tue Dec 19 2023 Ankit Jain <ankitja@vmware.com> 1.71.1-3
- Fix CVE-2023-40030
* Thu Sep 07 2023 Harinadh D <hdommaraju@vmware.com> 1.71.1-2
- version bump to use libssh2 1.11.0
* Thu Aug 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.71.1-1
- Fix CVE-2023-38497.
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 1.64.0-7
- Bump version as a part of ncurses upgrade to v6.4
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.64.0-6
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
