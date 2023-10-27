Summary:        A streaming media framework
Name:           gstreamer
Version:        1.21.90
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.xz
%define sha512  gstreamer=c363143685f022ac405147c11348957375b07de2d411fced0552999aebaed3c6885c03e7925f1e8451540ba2adaa659da1efc6b181e5c6fb053191ee81267f38

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  libxml2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-gobject-introspection
BuildRequires:  bison

Requires:       glib >= 2.68.4
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
Requires:       glib-devel >= 2.68.4
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
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.21.90-2
- Bump version as part of glib upgrade
*   Mon Jan 16 2023 Shivani Agarwal <shivania2@vmware.com> 1.21.90-1
-   Upgrade version to fix CVE-2021-3497, CVE-2021-3498, CVE-2021-3522, CVE-2021-2122, CVE-2021-1925, CVE-2021-1924, CVE-2021-1923, CVE-2021-1922, CVE-2021-1921, CVE-2021-1920
*   Tue Sep 06 2022 Shivani Agarwal <shivania2@vmware.com> 1.17.1-1
-   Upgrade version
*   Wed Jun 24 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-1
-   initial version
