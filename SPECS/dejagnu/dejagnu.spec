Summary:        DejaGnu test framework
Name:           dejagnu
Version:        1.6.2
Release:        1%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Source0:         https://ftp.gnu.org/pub/gnu/dejagnu/%{name}-%{version}.tar.gz
%define sha1    dejagnu=e8a28b8db857592f8f5d05a1c47bf2d2b823f1e9
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
Requires:       expect
BuildRequires:  expect-devel
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
%setup -q

%build
./configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

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
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.2-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 1.6-1
-   Upgraded to version 1.6
*   Thu Jul 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.5.3-1
-   Initial build. First version
