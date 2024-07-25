Summary:        DejaGnu test framework
Name:           dejagnu
Version:        1.6.2
Release:        2%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/pub/gnu/dejagnu/%{name}-%{version}.tar.gz
%define sha512 %{name}=ae527ce245871d49b84773d0d14b1ea6b2316c88097eeb84091a3aa885ff007eeaa1cd9c5b002d94a956d218451079b5e170561ffa43a291d9d82283aa834042

BuildArch:      noarch

BuildRequires:  expect-devel

Requires:       expect

%description
DejaGnu is a framework for testing other programs. Its purpose is to provide
a single front end for all tests. Think of it as a custom library of Tcl
procedures crafted to support writing a test harness. A test harness is the
testing infrastructure that is created to support a specific program or tool.
Each program can have multiple testsuites, all supported by a single test
harness. DejaGnu is written in Expect, which in turn uses Tcl.

%package devel
Summary:    Headers and development libraries for dejagnu
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   expect-devel

%description devel
Headers and development libraries for dejagnu

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/dejagnu/*
%{_infodir}/*
%exclude %{_infodir}/dir
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Sun Oct 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.6.2-2
- Fix spec issues
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.2-1
- Automatic Version Bump
* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 1.6-1
- Upgraded to version 1.6
* Thu Jul 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.5.3-1
- Initial build. First version
