%global debug_package       %{nil}
%define chromium_path       %{_libdir}/%{name}-browser
%define builddir            out/headless

Summary:        chromium
Name:           chromium
# Don't bump or upgrade version of this spec
# This is a special package & needs some manual effort
Version:        119.0.6045.176
Release:        1%{?dist}
License:        BSD 3
URL:            https://chromium.googlesource.com/chromium/src
Group:          System Utility
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/chromium/chromium/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=5d61521688875d198a185b304a82c855fa97ec871441bc65adb812fdabd5f92d8ba08dabe13b8ae81779582d829d18532e4adb9709fc4b50841c0ecc84f44d9d

# git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git
# tar cJf depot_tools-<short-commit-hash>.tar.xz depot_tools
Source1: depot_tools-eb48a6a.tar.xz
%define sha512 depot_tools=5b83f5afd6d50f525c25a0f70096de150e54b6b9c42f62900a34ea5142fb00bd1564470297af673a73af499391ef82e70a23972584906dc7595cb5e677abb606

Source2: headless.gn

BuildRequires: git
BuildRequires: nss-devel
BuildRequires: dbus-devel
BuildRequires: glib-devel
BuildRequires: glibc-devel
BuildRequires: nspr-devel
BuildRequires: ninja-build
BuildRequires: gperf

# TODO: need to revisit for aarch64
BuildArch: x86_64

Requires: glibc
Requires: nspr
Requires: nss-libs
Requires: open-sans-fonts

%description
Chromium is an open-source browser project that aims to build a safer, faster, and more stable way for all users to experience the web.

%prep
%autosetup -a0 -a1 -p1 -n src

%build
pushd %{_builddir}/src/build/linux/debian_bullseye_amd64-sysroot%{_libdir}/pkgconfig

cp glib-2.0.pc \
   dbus-1.pc \
   nss.pc \
   nspr.pc \
   %{_libdir}/pkgconfig

popd

mkdir -p %{builddir}
cp %{SOURCE2} %{builddir}/args.gn

%{_builddir}/src/depot_tools/gn gen %{builddir}

ninja -C %{builddir} headless_shell -j $(nproc)

%install
mkdir -p %{buildroot}%{chromium_path}
cp -pr %{builddir}/headless_lib_data.pak \
       %{builddir}/headless_lib_strings.pak \
       %{builddir}/headless_shell \
       %{builddir}/libvk_swiftshader.so* \
       %{builddir}/libvulkan.so* \
       %{builddir}/libEGL.so* \
       %{builddir}/libGLESv2.so* \
       %{builddir}/vk_swiftshader_icd.json \
       %{buildroot}%{chromium_path}

%files
%defattr(-,root,root)
%{chromium_path}

%changelog
* Mon Nov 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 119.0.6045.176-1
- Upgrade to v119.0.6045.176
* Thu Aug 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 116.0.5845.96-1
- Upgrade to v116.0.5845.93, fixes a bunch of CVEs
* Wed May 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 113.0.5672.95-1
- Initial packaging with Photon OS
