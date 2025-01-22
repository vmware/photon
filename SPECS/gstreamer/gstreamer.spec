Summary:        A streaming media framework
Name:           gstreamer
Version:        1.25.1
Release:        1%{?dist}
URL:            http://gstreamer.freedesktop.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz
%define sha512  gstreamer=8432f8ccdf84883d2e7764319429514d655248c1c6c7cc710bc76ffa0254b9bab98111281acf6233cc703f47c20a768c92d97839c3816df834bf6c35953febd7

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  glib-devel
BuildRequires:  libxml2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-gobject-introspection
BuildRequires:  bison

Requires:       glib
Requires:       libxml2

Provides:       pkgconfig(gstreamer-1.0)
Provides:       pkgconfig(gstreamer-base-1.0)

%description
GStreamer is a streaming media framework that enables applications to share a
common set of plugins for things like video encoding and decoding, audio encoding
and decoding, audio and video filters, audio visualisation, web streaming
and anything else that streams in real-time or otherwise.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel
Requires:       libxml2-devel
Requires:       gobject-introspection-devel
Requires:       python3-gobject-introspection

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -n gstreamer-%{version} -p1

%build
%meson \
    --auto-features=auto \
    %{nil}

%meson_build

%install
%meson_install

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{_bindir}
%{_libdir}/*.so*
%{_libexecdir}
%{_libdir}/gstreamer-1.0/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/gstreamer-1.0/*.so
%{_libdir}/girepository-1.0/*
%{_datadir}/*

%changelog
*   Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.25.1-1
-   update to 1.25.1
*   Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.22.7-2
-   Release bump for SRP compliance
*   Fri Dec 08 2023 Shivani Agarwal <shivania2@vmware.com> 1.22.7-1
-   Upgrade version
*   Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.21.3-2
-   Bump version as a part of libxml2 upgrade
*   Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.21.3-1
-   Automatic Version Bump
*   Tue Sep 06 2022 Shivani Agarwal <shivania2@vmware.com> 1.17.1-1
-   Upgrade version
*   Wed Jun 24 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-1
-   initial version
