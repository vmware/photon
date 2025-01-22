Summary:        The GStreamer Bad Plug-ins package contains a set a set of plug-ins that aren't up to par compared to the rest
Name:           gst-plugins-bad
Version:        1.25.1
Release:        1%{?dist}
URL:            http://gstreamer.freedesktop.org/
Group:          Applications/Multimedia
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz
%define sha512  %{name}=51a11258d3c3c58ba3860da3f1a85138fa60f5094259cd874fd4ca8bc17bb5df066e7e3cbebdcd1fbf384d13df4aaf168fe5503d302016936a2ac54d029d2063

Source1: license.txt
%include %{SOURCE1}

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
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.25.1-1
- Update to 1.25.1
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.22.7-4
- Release bump for SRP compliance
* Mon May 13 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.22.7-3
- Fix CVE-2023-50186
* Mon Jan 29 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.22.7-2
- Fix CVE-2024-0444
* Fri Dec 08 2023 Shivani Agarwal <shivania2@vmware.com> 1.22.7-1
- Upgrade version and Fix CVE-2023-40475 and CVE-2023-40476
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
