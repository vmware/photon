Summary:        Tool for static C/C++ code analysis
Name:           cppcheck
Version:        2.9.3
Release:        2%{?dist}
License:        GPLv3+
URL:            https://cppcheck.sourceforge.io
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/danmar/cppcheck/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=c75162b988415ee2ed255f7c648bdea1903c6a2471923f8430ab52f4e7c1ab8d2d1249585ac9db81f7c02fa90e8c0cf59d2bc0402d286c63344def5a171d9967

BuildRequires: build-essential

%if 0%{?with_check}
BuildRequires: libxml2-devel
BuildRequires: xmlstarlet
%endif

Requires: glibc
Requires: libgcc
Requires: libstdc++

%description
Cppcheck is a static analysis tool for C/C++ code. Cppcheck detects the types of bugs
that the compilers normally do not detect. The goal is to detect only real
errors in the code (i.e. have zero false positives).

%package addons
Summary: Add-ons package for Cppcheck.
Requires: python3
Requires: %{name} = %{version}-%{release}

%description addons
Add-ons package for Cppcheck.
Contains few helper python scripts.

%prep
%autosetup -p1

%build
export FILESDIR=%{_datadir}/%{name}
%make_build

%install
export FILESDIR=%{_datadir}/%{name}
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make test %{?_smp_mflags}
make checkcfg %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_datadir}/%{name}/cfg/*
%{_datadir}/%{name}/platforms/*
%{_bindir}/%{name}

%files addons
%defattr(-,root,root)
%{_bindir}/%{name}-htmlreport
%{_datadir}/%{name}/addons/*

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.3-2
- Bump version as a part of libxml2 upgrade
* Fri Nov 25 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.3-1
- Initial version
