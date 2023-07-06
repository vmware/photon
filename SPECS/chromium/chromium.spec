%global debug_package       %{nil}
%define chromium_path       %{_libdir}/%{name}-browser
%define builddir            out/headless

Summary:        chromium
Name:           chromium
# Don't bump or upgrade version of this spec
# This is a special package & needs some manual effort
Version:        113.0.5672.95
Release:        1%{?dist}
License:        BSD 3
URL:            https://chromium.googlesource.com/chromium/src
Group:          System Utility
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/chromium/chromium/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=a65de82d8a4392693440e861d62b80b23fc0730d57b3cdb63f4f307a9ed63eca4805def9a4dd0edce0ec258e8c2b38517ab5ed67ef02b62b5f6c673ade6b2563

# git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git
# tar cJf depot_tools-<short-commit-hash>.tar.xz depot_tools
Source1: depot_tools-872ac9bd3d.tar.xz
%define sha512 depot_tools=fdab499da273784dbe645cea6e178a5ea2910d8d2e26450a8be75df73f0fa97de60a27b5bcca77aad8e6e1f95653cebecf98ba9b6cd26351b920b1f3d71a9f0d

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
* Wed May 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 113.0.5672.95-1
- Initial packaging with Photon OS
