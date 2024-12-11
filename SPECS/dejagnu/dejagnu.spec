Summary:        DejaGnu test framework
Name:           dejagnu
Version:        1.6.2
Release:        3%{?dist}
URL:            http://www.gnu.org/software/%{name}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/pub/gnu/dejagnu/%{name}-%{version}.tar.gz
%define sha512 %{name}=ae527ce245871d49b84773d0d14b1ea6b2316c88097eeb84091a3aa885ff007eeaa1cd9c5b002d94a956d218451079b5e170561ffa43a291d9d82283aa834042

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  expect-devel

Requires:       expect
Requires(post): texinfo
Requires(postun): texinfo

%description
DejaGnu is a framework for testing other programs. Its purpose is to provide
a single front end for all tests. Think of it as a custom library of Tcl
procedures crafted to support writing a test harness. A test harness is the
testing infrastructure that is created to support a specific program or tool.
Each program can have multiple testsuites, all supported by a single test
harness. DejaGnu is written in Expect, which in turn uses Tcl.

%package devel
Summary: Headers and development libraries for dejagnu
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: expect-devel

%description devel
Headers and development libraries for dejagnu

%prep
%autosetup -p1

%build
sh ./configure --prefix=%{_usr}

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%post
%{_bindir}/install-info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun
%{_bindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

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
*   Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.6.2-3
-   Release bump for SRP compliance
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6.2-2
-   Release bump for SRP compliance
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.2-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 1.6-1
-   Upgraded to version 1.6
*   Thu Jul 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.5.3-1
-   Initial build. First version
