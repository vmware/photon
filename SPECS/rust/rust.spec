Summary:        Rust Programming Language
Name:           rust
Version:        1.58.1
Release:        2%{?dist}
License:        Apache License Version 2.0 and MIT
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://static.rust-lang.org/dist/%{name}c-%{version}-src.tar.xz
%define sha512  %{name}c-%{version}-src=eff3279d2e519343cea542a9ae2daab592e44f35af344e33ff43ed55fc7c824511790d1991dd36a603d12465de8c3688e7194c2b9557f288c587ffa04738c2ce
Patch0:         0001-fix-respect-umask-when-unpacking-.crate-files.patch
Patch1:         0002-fix-clear-cache-for-old-.cargo-ok-format.patch
BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  glibc
BuildRequires:  binutils
BuildRequires:  python3
BuildRequires:  curl-devel
BuildRequires:  ninja-build
Requires:       glibc
Requires:       glibc-devel
Requires:       gcc
Requires:       libstdc++
Requires:       openssl
Requires:       binutils

%description
Rust Programming Language

%prep
%autosetup -p1 -n %{name}c-%{version}-src

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
* Fri Aug 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.58.1-2
- Fix CVE-2023-38497.
* Sat Jan 22 2022 Ankit Jain <ankitja@vmware.com> 1.58.1-1
- Updated to 1.58.1 to fix CVE-2022-21658
* Thu Oct 28 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-5
- Fixes CVE-2021-42574
* Mon Aug 23 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-4
- Fixes CVE-2021-29922
* Tue May 04 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-3
- Fixes CVE-2020-36323
* Wed Apr 28 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-2
- Fixes CVE-2021-28876,CVE-2021-28878,CVE-2021-28879
* Mon Apr 19 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-1
- Update to latest version to fix CVE-2021-31162
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 1.34.2-2
- Added for ARM Build
* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.34.2-1
- Initial build. First version
