Summary:        The GStreamer Bad Plug-ins package contains a set a set of plug-ins that aren't up to par compared to the rest
Name:           gst-plugins-bad
Version:        1.21.3
Release:        4%{?dist}
License:        LGPLv2
URL:            http://gstreamer.freedesktop.org/
Group:          Applications/Multimedia
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz
%define sha512  %{name}=706b77adcb9d73cbfa5148eacc5c9efc4ad904d25a23b70b5bd80b0891c94ac5c5400416de1cf9aa86558e606d1928af9bae7acc68491ca7414f63604fa6cf71

Patch0:         CVE-2023-37329.patch
Patch1:         CVE-2023-40474.patch
Patch2:         CVE-2023-40475.patch
Patch3:         CVE-2023-44429.patch
Patch4:         CVE-2023-44446.patch

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  gstreamer-plugins-base-devel
Requires:       gstreamer-plugins-base

%description
The GStreamer Good Plug-ins is a set of plug-ins considered by the GStreamer developers
to have good quality code, correct functionality, and the preferred license (LGPL).
A wide range of video and audio decoders, encoders, and filters are included.

%package        devel
Summary:        GStreamer Plugin Library Headers
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gstreamer-plugins-base-devel

%description    devel
The GStreamer Bad Plug-ins package contains a set a set of plug-ins that aren't up to par compared to the rest

%prep
%autosetup -p1

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
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/gstreamer-1.0/*.so
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_libdir}/girepository-1.0
%{_includedir}/gstreamer-1.0
%{_datadir}/locale
%{_datadir}/gstreamer-1.0
%{_datadir}/gir-1.0

%changelog
* Fri Nov 24 2023 Shivani Agarwal <shivania2@vmware.com> 1.21.3-4
- Fix CVE-2023-44429 and CVE-2023-44446
* Thu Nov 16 2023 Shivani Agarwal <shivania2@vmware.com> 1.21.3-3
- Fix CVE-2023-40474, CVE-2023-40475
* Thu Sep 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.21.3-2
- Fix CVE-2023-37329
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.21.3-1
- Automatic Version Bump
* Tue Sep 06 2022 Shivani Agarwal <shivania2@vmware.com> 1.17.1-1
- Upgrade version
* Mon Jul 13 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-1
- initial version
