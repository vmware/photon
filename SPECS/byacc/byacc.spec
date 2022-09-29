%define byaccdate 20220128

Summary:    Berkeley Yacc, a parser generator
Name:       byacc
Version:    2.0.20220128
Release:    2%{?dist}
License:    Public Domain
Group:      Development/Tools
Vendor:     VMware, Inc.
URL:        https://byaccj.sourceforge.net
Distribution: Photon

Source0: https://invisible-island.net/archives/%{name}/%{name}-%{byaccdate}.tgz
%define sha512 %{name}=e8ae4c56f5be4cc0ef1d281c43f02c6296fdc40f630269f2a61af511f270ae059ad185b9718190b8133018f7b74b7ca6f84ced5d63a359960b52ea2a3ef562ea

BuildRequires: gcc
BuildRequires: make

Conflicts: bison

%description
This package provides a parser generator utility that reads a grammar
specification from a file and generates an LR(1) parser for it.  The
parsers consist of a set of LALR(1) parsing tables and a driver
routine written in the C programming language.  It has a public domain
license which includes the generated C.

If you are going to do development on your system, you will want to install
this package.

%prep
%autosetup -p1 -n %{name}-%{byaccdate}

%build
%configure --disable-dependency-tracking

%make_build

%install
%make_install
ln -sv yacc %{buildroot}%{_bindir}/%{name}
ln -sv yacc.1 %{buildroot}%{_mandir}/man1/%{name}.1

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files
%{_bindir}/yacc
%{_bindir}/%{name}
%{_mandir}/man1/yacc.1*
%{_mandir}/man1/%{name}.1*

%changelog
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.20220128-2
- Spec fixes
* Tue Sep 13 2022 Roye Eshed <eshedr@vmware.com> 2.0.20220128-1
- Adding of the byacc spec file for photon based on the Fedora SPEC file.
