%global security_hardening none
Summary:        Memory Management Debugger.
Name:           valgrind
Version:        3.20.0
Release:        2%{?dist}
URL:            http://valgrind.org
Group:          Development/Debuggers
Source0:        http://valgrind.org/downloads/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  pkg-config
BuildRequires:  sed

%description
Valgrind is a GPL'd system for debugging and profiling Linux programs. With
Valgrind's tool suite you can automatically detect many memory management and
threading bugs, avoiding hours of frustrating bug-hunting, making your programs
more stable. You can also perform detailed profiling to help speed up your
programs.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/valgrind
%{_libdir}/valgrind
%{_libdir}/pkgconfig/*
%{_libexecdir}/*
%{_mandir}/*/*
%{_datadir}/doc/valgrind/*

%changelog
*   Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 3.20.0-2
-   Release bump for SRP compliance
*   Tue Nov 1 2022 Oliver Kurth <okurth@vmware.com> 3.20.0-1
-   Update to version 3.20.0
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 3.19.0-1
-   Automatic Version Bump
*   Wed Aug 18 2021 Oliver Kurth <okurth@vmware.com> 3.17.0-1
-   Update to version 3.17.0
*   Wed Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 3.16.1-1
-   Automatic Version Bump
*   Tue Jan 07 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.15.0-1
-   Update to version 3.13.0
*   Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 3.13.0-1
-   Update to version 3.13.0
*   Tue Sep 19 2017 Bo Gan <ganb@vmware.com> 3.12.0-2
-   Fix make check issue
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.12.0-1
-   Updated to version 3.12.0.
*   Fri Aug 05 2016 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-1
-   Initial Build.
