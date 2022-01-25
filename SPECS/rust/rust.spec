Summary:        Rust Programming Language
Name:           rust
Version:        1.58.1
Release:        1%{?dist}
License:        Apache License Version 2.0 and MIT
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
# Manually created Source tar which is equal to
# Source0 + .git as it requires git hooks at build time
Source0:        https://github.com/rust-lang/rust/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=57aaff24bee94720e936d687c390032acb54114e
BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  glibc
BuildRequires:  binutils
BuildRequires:  python3
BuildRequires:  curl-devel
BuildRequires:  ninja-build

Requires:  glibc
Requires:  gcc
Requires:  libstdc++
Requires:  openssl

%description
Rust Programming Language

%prep
%autosetup -p1

%build
sh ./configure --prefix=%{_prefix} --enable-extended --tools="cargo"
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}%{_libdir} -maxdepth 1 -type f -name '*.so' -exec chmod -v +x '{}' '+'
rm %{buildroot}%{_docdir}/%{name}/html/.lock
rm %{buildroot}%{_docdir}/%{name}/*.old

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
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
%{_docdir}/%{name}/html/.stamp
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
*   Sat Jan 22 2022 Ankit Jain <ankitja@vmware.com> 1.58.1-1
-   Updated to 1.58.1 to fix CVE-2022-21658
*   Thu Oct 28 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-5
-   Fixes CVE-2021-42574
*   Mon Aug 23 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-4
-   Fixes CVE-2021-29922
*   Tue May 04 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-3
-   Fixes CVE-2020-36323
*   Wed Apr 28 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-2
-   Fixes CVE-2021-28876,CVE-2021-28878,CVE-2021-28879
*   Mon Apr 19 2021 Ankit Jain <ankitja@vmware.com> 1.51.0-1
-   Update to latest version to fix CVE-2021-31162
*   Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 1.34.2-2
-   Added for ARM Build
*   Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.34.2-1
-   Initial build. First version
