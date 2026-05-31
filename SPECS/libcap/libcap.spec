%global build_if %{photon_subrelease} >= 91

Summary:        Libcap
Name:           libcap
Version:        2.77
Release:        4%{?dist}
URL:            https://www.gnu.org/software/hurd/community/gsoc/project_ideas/libcap.html
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  elfutils

Requires:       %{name}-minimal = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description
The libcap package implements the user-space interfaces to the POSIX 1003.1e capabilities available in Linux kernels.
These capabilities are a partitioning of the all powerful root privilege into a set of distinct privileges.

%package        libs
Conflicts:      %{name} < 2.77-1
Summary:        Libraries for %{name}

%description    libs
This package contains minimal set of shared %{name} libraries.

%package        minimal
Conflicts:      %{name} < 2.77-1
Requires:       %{name}-libs = %{version}-%{release}
Summary:        Minimal set of %{name} tools

%description    minimal
%{summary}

%package        devel
Summary:        Development files for libcap
Requires:       %{name} = %{version}-%{release}

%description    devel
The libcap-devel package contains libraries, header files and documentation for developing applications that use libcap.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name} < 2.77-1

%description    doc
%{summary}

%prep
%autosetup -p1
# NOTE: binutils readelf has some issue while creating debuginfo rpms
# 'readelf: Error: Unable to find program interpreter name'
#
# It happens due to:
# https://git.kernel.org/pub/scm/libs/libcap/libcap.git/tree/libcap/Makefile#n30
# Working around it for now
ln -sfrv %{_bindir}/eu-readelf %{_bindir}/readelf

%build
%make_build

%install
%make_install %{?_smp_mflags} \
  prefix=%{_prefix} \
  RAISE_SETFCAP=no \
  LIBDIR=%{_libdir}

chmod -v 755 %{buildroot}%{_libdir}/%{name}.so

%if 0%{?with_check}
%check
%make_build test
%endif

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%exclude %{_sbindir}/getcap
%exclude %{_sbindir}/setcap
%exclude %{_libdir}/libcap.so.*
%{_libdir}/libpsx.so.*
%{_sbindir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/libcap.so.*

%files minimal
%defattr(-,root,root)
%{_sbindir}/getcap
%{_sbindir}/setcap

%files devel
%defattr(-,root,root)
%{_includedir}/*
%exclude %{_libdir}/libcap.a
%exclude %{_libdir}/libpsx.a
%{_libdir}/pkgconfig/*
%{_libdir}/libcap.so
%{_libdir}/libpsx.so

%files doc
%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%changelog
*   Sun May 31 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.77-4
-   Workaround debuginfo build issue
*   Thu May 14 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.77-3
-   Build for subrelease >= 91
*   Sat Mar 07 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.77-2
-   Fix aarch64 build, cleanup spec
*   Mon Feb 09 2026 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 2.77-1
-   Update to v2.77 and split libcap into sub-packages
*   Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.66-4
-   Release bump for SRP compliance
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.66-3
-   Release bump for SRP compliance
*   Fri Jun 02 2023 Piyush Gupta <gpiyush@vmware.com> 2.66-2
-   Fix CVE-2023-2602, CVE-2023-2603.
*   Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 2.66-1
-   Automatic Version Bump
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.64-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.49-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 2.43-1
-   Automatic Version Bump
*   Wed Jul 29 2020 Tapas Kundu <tkundu@vmware.com> 2.31-1
-   Update to 2.31
*   Tue Nov 26 2019 Alexey Makhalov <amakhalov@vmware.com> 2.25-9
-   Cross compilation support
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.25-8
-   Aarch64 support
*   Wed Aug 09 2017 Danut Moraru <dmoraru@vmware.com> 2.25-7
-   Remove capsh test that runs chroot already in chroot, failing due to
    expected environment/dependencies not available
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.25-6
-   Remove attr deps.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.25-5
-   Moved man3 to devel subpackage.
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.25-4
-   BuildRequired attr-devel.
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.25-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25-2
-   GA - Bump release of all rpms
*   Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 2.25-1
-   Updating Version.
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.24-2
-   Moving static lib files to devel package.
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.24-1
-   Initial version.
