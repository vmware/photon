Summary:        The GL Vendor-Neutral Dispatch library
Name:           libglvnd
Version:        1.4.0
Release:        5%{?dist}
License:        MIT
URL:            https://github.com/NVIDIA/libglvnd
Group:          Development/Libraries/C and C++
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/NVIDIA/libglvnd/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=2a1cf975a0453c4e3777e4380b1084d9d5ddfaf7fd96d97f7e503c1a3b46b2234245939626d5c816da8ad41b88dbf67ee0a8dbb7cc755852ed0b75a67caea8b0

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  libX11-devel
BuildRequires:  libxml2-devel
BuildRequires:  proto

%description
Vendor-neutral dispatch layer for arbitrating OpenGL API calls between
multiple vendors on a per-screen basis, as described by Andy Ritger's
OpenGL ABI proposal.

%package        devel
Summary:        Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-opengl = %{version}-%{release}
Requires:       %{name}-gles = %{version}-%{release}
Requires:       %{name}-egl = %{version}-%{release}
Requires:       %{name}-glx = %{version}-%{release}

%description    devel
Vendor-neutral dispatch layer for arbitrating OpenGL API calls between
multiple vendors on a per-screen basis, as described by Andy Ritger's
OpenGL ABI proposal. This package contains the required files for
development.

%package        opengl
Summary:        OpenGL support for libglvnd
Requires:       %{name} = %{version}-%{release}

%description    opengl
libOpenGL is the common dispatch interface for the workstation OpenGL API.

%package        gles
Summary:        GLES support for libglvnd
Requires:       %{name} = %{version}-%{release}

%description    gles
libGLESv is the common dispatch interface for the workstation GLES API.

%package        egl
Summary:        EGL support for libglvnd
Requires:       %{name} = %{version}-%{release}

%description    egl
libEGL is the common dispatch interface for the workstation EGL API.

%package        glx
Summary:        GLX support for libglvnd
Requires:       %{name} = %{version}-%{release}

%description    glx
libGL and libGLX are the common dispatch interface for the workstation GLX API.

%prep
%autosetup -p1

%build
%meson \
      -Degl=true \
      --buildtype=release \
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
%defattr(-,root,root)
%{_libdir}/libGLdispatch.so.0*

%ldconfig_scriptlets opengl

%files opengl
%defattr(-,root,root)
%{_libdir}/libOpenGL.so.0*

%ldconfig_scriptlets gles

%files gles
%defattr(-,root,root)
%{_libdir}/libGLES*.so.*

%ldconfig_scriptlets glx

%files glx
%defattr(-,root,root)
%{_libdir}/libGL.so.*
%{_libdir}/libGLX.so.*

%ldconfig_scriptlets egl

%files egl
%defattr(-,root,root)
%{_libdir}/libEGL*.so.*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/EGL/
%dir %{_includedir}/GL/
%dir %{_includedir}/GLES/
%dir %{_includedir}/GLES2/
%dir %{_includedir}/GLES3/
%dir %{_includedir}/KHR/
%{_includedir}/EGL/*.h
%{_includedir}/GL/*.h
%{_includedir}/GLES/*.h
%{_includedir}/GLES2/*.h
%{_includedir}/GLES3/*.h
%{_includedir}/KHR/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/gl*.pc
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/pkgconfig/opengl.pc
%dir %{_includedir}/glvnd/
%{_includedir}/glvnd/*.h
%{_libdir}/pkgconfig/libglvnd.pc

%changelog
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.4.0-5
- Bump version as a part of libxml2 upgrade
* Sat Sep 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-4
- Fix devel package requires
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.4.0-3
- Bump version as a part of libX11 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.4.0-2
- Bump version as a part of libxml2 upgrade
* Fri Sep 2 2022 Shivani Agarwal <shivania2@vmware.com> 1.4.0-1
- Initial Version
