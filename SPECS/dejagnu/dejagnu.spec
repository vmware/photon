Summary:        DejaGnu test framework
Name:           dejagnu
Version:        1.5.3
Release:        1%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Source0:         https://ftp.gnu.org/pub/gnu/dejagnu/dejagnu-1.5.3.tar.gz
%define sha1    dejagnu=d81288e7d7bd38e74b7fee8e570ebfa8c21508d9
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
*   Thu Jul 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.5.3-1
-   Initial build. First version
