%define byaccdate 20220128

Summary: Berkeley Yacc, a parser generator
Name: byacc
Version: 2.0.20220128
Release: 1%{?dist}
License: Public Domain
Group: Development/Tools
Vendor: VMware, Inc.
Distribution: Photon
URL: http://invisible-island.net/%{name}/%{name}.html
Source: https://invisible-island.net/archives/%{name}/%{name}-%{byaccdate}.tgz

BuildRequires: gcc
BuildRequires: make
%define sha512 %{name}=e8ae4c56f5be4cc0ef1d281c43f02c6296fdc40f630269f2a61af511f270ae059ad185b9718190b8133018f7b74b7ca6f84ced5d63a359960b52ea2a3ef562ea

%description
This package provides a parser generator utility that reads a grammar
specification from a file and generates an LR(1) parser for it.  The
parsers consist of a set of LALR(1) parsing tables and a driver
routine written in the C programming language.  It has a public domain
license which includes the generated C.

If you are going to do development on your system, you will want to install
this package.

%prep
%autosetup -n byacc-%{byaccdate}

# Revert default stack size back to 10000
# https://bugzilla.redhat.com/show_bug.cgi?id=743343
find . -type f -name \*.c -print0 |
  xargs -0 sed -i 's/YYSTACKSIZE 500/YYSTACKSIZE 10000/g'

%build
%configure --disable-dependency-tracking

%make_build

%install
%make_install
ln -s yacc %{buildroot}%{_bindir}/byacc
ln -s yacc.1 %{buildroot}%{_mandir}/man1/byacc.1

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%files
%doc ACKNOWLEDGEMENTS CHANGES NEW_FEATURES NOTES NO_WARRANTY README
%{_bindir}/yacc
%{_bindir}/byacc
%{_mandir}/man1/yacc.1*
%{_mandir}/man1/byacc.1*

%changelog
* Tue Sep 13 2022 Roye Eshed <eshedr@vmware.com> - 2.0.20220128-1
- Adding of the byacc spec file for photon based on the Fedora SPEC file.
