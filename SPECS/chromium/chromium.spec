%global debug_package       %{nil}
%define chromium_path       %{_libdir}/%{name}-browser
%define builddir            out/headless

Summary:        chromium
Name:           chromium
# Don't bump or upgrade version of this spec
# This is a special package & needs some manual effort
Version:        123.0.6283.1
Release:        1%{?dist}
License:        BSD 3
URL:            https://chromium.googlesource.com/chromium/src
Group:          System Utility
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/chromium/chromium/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=f17ee035fc2e2a6c6a220d008574f0570980a76a678a7d9ed86c24779246f9f2abc521328c1369556c389c1c0f1dc57d957d2766adcdcc12f121fb127f747118

# git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git
# tar cJf depot_tools-<short-commit-hash>.tar.xz depot_tools
Source1: depot_tools-af6eabf.tar.xz
%define sha512 depot_tools=78a880d9e57c2954aa5a77344c716e41a113e85238df6b326baee3b7731d9f9491a2cc789fb31823f9142f20440da907562a2cb4681b3985bd069dbf71b4a5da

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

> %{SOURCE0}

%files
%defattr(-,root,root)
%{chromium_path}

%changelog
* Tue Feb 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 123.0.6283.1-1
- Upgrade to v123.0.6283.1
* Fri Dec 01 2023 Shreenidhi Shedi <sshedi@vmware.com> 119.0.6045.176-2
- Ignore chromium source tarball while creating src rpm.
- If packages, it results in a huge src rpm & will cause signing issues
* Mon Nov 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 119.0.6045.176-1
- Upgrade to v119.0.6045.176
* Thu Aug 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 116.0.5845.96-1
- Upgrade to v116.0.5845.93, fixes a bunch of CVEs
* Wed May 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 113.0.5672.95-1
- Initial packaging with Photon OS
