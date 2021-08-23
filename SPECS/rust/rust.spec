Summary:        Rust Programming Language
Name:           rust
Version:        1.51.0
Release:        4%{?dist}
License:        Apache License Version 2.0 and MIT
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
# Manually created Source tar which is equal to
# Source0 + .git as it requires git hooks at build time
Source0:        https://github.com/rust-lang/rust/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=4f3ff7080e3adcbbb336b8569c7a36096ad7e12e
Patch0:         CVE-2021-31162.patch
Patch1:         CVE-2021-28876.patch
Patch2:         0001-Turn-may_have_side_effect-into-an-associated-constan.patch
Patch3:         CVE-2021-28879.patch
Patch4:         CVE-2021-28878.patch
Patch5:         CVE-2020-36323.patch
Patch6:         CVE-2021-29922.patch
BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  glibc
BuildRequires:  binutils
BuildRequires:  python2
BuildRequires:  curl-devel
BuildRequires:  ninja-build

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
