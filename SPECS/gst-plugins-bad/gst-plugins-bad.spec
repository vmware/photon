Summary:        The GStreamer Bad Plug-ins package contains a set a set of plug-ins that aren't up to par compared to the rest
Name:           gst-plugins-bad
Version:        1.28.7
Release:        1%{?dist}
License:        LGPLv2
URL:            http://gstreamer.freedesktop.org/
Group:          Applications/Multimedia
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz
%define sha512 %{name}=2ae81e1584fa1e4450a039780c22510c67ab6d88fdbec5dccb5407c1256e59834aad83784dadc994c014ed8334ac40de96b5a239a4521b186d1462338328bc25

Patch0: tensordecoders-g_alloca0-fallback.patch

BuildRequires:  meson >= 1.4.0
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
* Mon Nov 09 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.28.7-1
- Version upgrade to 1.28.7
- Add g_alloca0 fallback for glib < 2.72
* Thu Jun 25 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.26.11-2
- Fix CVE-2026-52718, CVE-2026-52719, CVE-2026-52720, CVE-2026-52721, CVE-2026-52722,
  CVE-2026-53701, CVE-2026-53702
* Tue May 12 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.26.11-1
- Version upgrade to 1.26.11
* Fri Mar 27 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.25.1-3
- Fix CVE-2026-3084 and CVE-2026-3082
* Mon Jan 05 2026 Tapas Kundu <tapas.kundu@broadcom.com> 1.25.1-2
- Fix CVE-2025-3887
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.25.1-1
- Update to 1.25.1
* Mon May 13 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.22.7-3
- Fix CVE-2023-50186
* Mon Jan 29 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.22.7-2
- Fix CVE-2024-0444
* Fri Nov 24 2023 Shivani Agarwal <shivania2@vmware.com> 1.22.7-1
- Upgrade version and Fix CVE-2023-44429 and CVE-2023-44446
* Tue Nov 14 2023 Kuntal Nayak <nkuntal@vmware.com> 1.17.1-4
- Fix CVE-2023-40474
* Thu Sep 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.17.1-3
- Fix CVE-2023-37329
* Tue Mar 21 2023 Shivani Agarwal <shivania2@vmware.com> 1.17.1-2
- Fix CVE-2021-3185
* Tue Sep 06 2022 Shivani Agarwal <shivania2@vmware.com> 1.17.1-1
- Upgrade version
* Mon Jul 13 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-1
- initial version
