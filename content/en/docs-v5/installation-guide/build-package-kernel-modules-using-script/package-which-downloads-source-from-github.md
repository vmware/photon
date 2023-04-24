---
title: Refer an External Source
weight: 5
---

This example shows how to build a package that downloads the source files from an external website like GitHub. To build the package, you need to run the script with `libdrm.spec` as an argument, where `libdrm.spec` is the RPM specification file.

```
./photon/tools/scripts/build_spec.sh ./photon/tools/examples/build_spec/user_package_example/libdrm.spec
```


The following are the contents of the `libdrm.spec` file:

```
Summary:        user space library for accessing the DRM.
Name:           libdrm
Version:        2.4.110
Release:        1%{?dist}
License:        MIT
URL:            http://dri.freedesktop.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://dri.freedesktop.org/libdrm/%{name}-%{version}.tar.xz

BuildRequires:  meson
BuildRequires:  libpciaccess-devel
Requires:       libpciaccess
Provides:       pkgconfig(libdrm)

%description
libdrm provides a user space library for accessing the DRM, direct rendering manager, on operating systems that support the ioctl interface. libdrm is a low-level library, typically used by graphics drivers such as the Mesa DRI drivers, the X drivers, libva and similar projects.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
libdrm provides a user space library for accessing the DRM, direct rendering manager, on operating systems that support the ioctl interface. libdrm is a low-level library, typically used by graphics drivers such as the Mesa DRI drivers, the X drivers, libva and similar projects.

%prep
%autosetup -p1

%build
CONFIGURE_OPTS=(
        -Dintel=false
        -Dradeon=false
        -Damdgpu=true
        -Dnouveau=false
        -Dvmwgfx=false
        -Dlibkms=false
)

%meson "${CONFIGURE_OPTS[@]}"
meson --prefix=%{_prefix} build

%install
DESTDIR=%{buildroot}/ ninja -C build install

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/lib*
%{_datadir}/libdrm/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig*
```


#### Build Logs

The following logs indicate the steps that the script performs internally:

```
0. Build Script Version: 1.1
1. Create sandbox
        Use local build template image OK
2. Prepare build environment
        Create source folder OK
        Copy sources from ./photon/tools/examples/build_spec/user_package_example OK
        Download libdrm-2.4.110.tar.xz OK
        install createrepo OK
        createrepo  OK
        Create local repo in sandbox OK
        makecache OK
        Install build requirements OK
3. Build Binary and Source Package
        Run rpmbuild OK
        Delete SOURCES OK
4. Destroy sandbox
        Stop container OK
        Remove container OK
Build completed. RPMS are in './photon/tools/examples/build_spec/user_package_example/stage' folder
```