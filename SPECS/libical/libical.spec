Summary:        Libical — an implementation of iCalendar protocols and data formats
Name:           libical
Version:        3.0.14
Release:        7%{?dist}
License:        MPL-2.0
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/libical
Source0:        https://github.com/libical/libical/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=36da5516672976c71b049a12af36164d91f9b655f81f1884766558149f25e80c30e64d15da848842f8a629295d708f39ce6fa63a3b0da39b5cbeb91911a4e6d8

BuildRequires:  cmake
BuildRequires:  glib-devel
BuildRequires:  libxml2-devel
BuildRequires:  icu-devel

%if 0%{?with_check}
BuildRequires:  tzdata
%endif

Requires:       libxml2
Requires:       icu

%description
Libical is an Open Source implementation of the iCalendar protocols and
protocol data units. The iCalendar specification describes how calendar
clients can communicate with calendar servers so users can store their
calendar data and arrange meetings with other users.

%package        devel
Summary:        Development files for Libical
Group:          Development/System
Requires:       %{name} = %{version}-%{release}
Requires:       icu-devel

%description    devel
The libical-devel package contains libraries and header files for developing
applications that use libical.

%prep
%autosetup -p1

%build
%cmake -DENABLE_GTK_DOC=OFF \
       -DCMAKE_BUILD_TYPE=Debug \
       -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
       -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir} \

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
make test ARGS="-V" %{?_smp_mflags}
%endif

%ldconfig_scriptlets

%files
%{_libdir}/*.so.*
%{_libdir}/cmake/LibIcal/*.cmake
%{_libexecdir}/%{name}/ical-glib-src-generator
%doc COPYING TODO

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 3.0.14-7
- Bump version as a part of libxml2 upgrade
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 3.0.14-6
- Bump version as a part of libxml2 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.0.14-5
- Bump version as a part of libxml2 upgrade
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.14-4
- Bump version as a part of icu upgrade
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.14-3
- Bump version as a part of icu upgrade
* Tue Jun 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.14-2
- Fix deliverables packaging
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.0.14-1
- Automatic Version Bump
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 3.0.10-3
- Release bump up to use libxml2 2.9.12-1.
* Wed Jun 30 2021 Tapas Kundu <tkundu@vmware.com> 3.0.10-2
- Need libxml2 in requires
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.0.10-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.8-1
- Automatic Version Bump
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 3.0.7-1
- Initial version.
