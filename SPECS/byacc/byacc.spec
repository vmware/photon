%define byaccdate 20221106

Summary:       Berkeley Yacc, a parser generator
Name:          byacc
Version:       2.0.20221106
Release:       2%{?dist}
Group:         Development/Tools
Vendor:        VMware, Inc.
URL:           https://byaccj.sourceforge.net
Distribution:  Photon

Source0:       https://invisible-island.net/archives/%{name}/%{name}-%{byaccdate}.tgz
%define sha512 %{name}=866933b4eb2296565ce70b4ade565e4679f3b652715f0066072bbcc42b95389fa47a2f96cd03de577807dcc49bf453b1d4f7e22b96c80fef1aa66898d3de5d5c

Source1: license.txt
%include %{SOURCE1}

BuildRequires: gcc
BuildRequires: make

Conflicts:     bison

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
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 2.0.20221106-2
- Release bump for SRP compliance
* Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.20221106-1
- Automatic Version Bump
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.20220128-2
- Spec fixes
* Tue Sep 13 2022 Roye Eshed <eshedr@vmware.com> 2.0.20220128-1
- Adding of the byacc spec file for photon based on the Fedora SPEC file.
