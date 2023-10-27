Summary:      Libical — an implementation of iCalendar protocols and data formats
Name:         libical
Version:      3.0.8
Release:      6%{?dist}
License:      MPL-2.0
Group:        System Environment/Libraries
Vendor:       VMware, Inc.
Distribution: Photon
URL:          https://github.com/libical

Source0: https://github.com/libical/libical/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=ce015e6d4c1c7cb4af7b45748ce8251c663f80f6a4357ddff6a97796642619abe882f4cadeca10cabeb1b25577869f436da15bca882e032eb3ff0475f6010d8b

BuildRequires:  cmake
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  libxml2-devel

Requires:       libxml2

%description
Libical is an Open Source implementation of the iCalendar protocols and
protocol data units. The iCalendar specification describes how calendar
clients can communicate with calendar servers so users can store their
calendar data and arrange meetings with other users.

%package    devel
Summary:    Development files for Libical
Group:      Development/System
Requires:   %{name} = %{version}-%{release}

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/cmake/LibIcal/*.cmake
%doc COPYING TODO

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.0.8-6
- Bump version as part of glib upgrade
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.8-5
- Use cmake macros
* Sat Feb 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.8-4
- Drop libdb support
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 3.0.8-3
- Release bump up to use libxml2 2.9.12-1.
* Wed Jun 30 2021 Tapas Kundu <tkundu@vmware.com> 3.0.8-2
- Need libxml2 in requires
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.8-1
- Automatic Version Bump
* Mon Jan 6 2020 Ajay Kaher <akaher@vmware.com> 3.0.7-1
- Initial version
