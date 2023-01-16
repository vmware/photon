Summary:        GStreamer streaming media framework plug-ins
Name:           gstreamer-plugins-base
Version:        1.17.1
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org
Group:          Applications/Multimedia
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-%{version}.tar.xz
%define sha512 gst-plugins-base=4b03e508d2e8de00690d47018aede46d1896bc19c829e4f3ad673c37ad33edb53da88b196b995bb7fb68076c0e47e0953a6a610519ae57edaf8294e41d94f2ee

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  gstreamer-devel
BuildRequires:  pango-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  fribidi-devel

Requires:       gstreamer
Requires:       pango
Requires:       alsa-lib
Requires:       libX11
Requires:       libXext
Requires:       cairo

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%package        devel
Summary:        GStreamer Plugin Library Headers
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gstreamer-devel
Requires:       pango-devel
Requires:       cairo-devel
Requires:       alsa-lib-devel
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       fribidi-devel

%description    devel
GStreamer Plugins Base library development and header files.

%prep
%autosetup -n gst-plugins-base-%{version} -p1

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
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/gst-discoverer-1.0
%{_bindir}/gst-play-1.0
%{_bindir}/gst-device-monitor-1.0
%{_mandir}/man1/gst-discoverer-1.0*
%{_mandir}/man1/gst-play-1.0*
%{_mandir}/man1/gst-device-monitor-1.0*
%{_libdir}/*.so.*
%{_libdir}/gstreamer-1.0/*.so

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/gstreamer-1.0/*.so
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/*

%changelog
*   Mon Jan 16 2023 Shivani Agarwal <shivania2@vmware.com> 1.17.1-2
-   Upgrade version to build with new gstreamer
*   Tue Sep 06 2022 Shivani Agarwal <shivania2@vmware.com> 1.17.1-1
-   Upgrade version
*   Wed Nov 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-2
-   Updated build requires & requires to build with Photon 2.0
*   Thu Jun 25 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-1
-   initial version
