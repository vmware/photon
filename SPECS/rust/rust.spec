Summary:        Rust Programming Language
Name:           rust
Version:        1.55.0
Release:        2%{?dist}
License:        Apache License Version 2.0 and MIT
URL:            https://github.com/rust-lang/rust
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://static.rust-lang.org/dist/%{name}c-%{version}-src.tar.xz
%define sha1    %{name}c-%{version}-src=3fd8c1e1d44f95621499d245d0be00c4945347fb

BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  glibc
BuildRequires:  binutils
BuildRequires:  python3
BuildRequires:  curl-devel
BuildRequires:  ninja-build

%description
Rust Programming Language

%prep
%autosetup -p1 -n %{name}c-%{version}-src

%build
sh ./configure --prefix=%{_prefix} --enable-extended --tools="cargo"
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}%{_libdir} -maxdepth 1 -type f -name '*.so' -exec chmod -v +x '{}' '+'
rm %{buildroot}%{_docdir}/%{name}/html/.lock %{buildroot}%{_docdir}/%{name}/*.old

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
