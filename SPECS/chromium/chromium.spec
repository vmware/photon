%global debug_package       %{nil}
%define chromium_path       %{_libdir}/%{name}-browser
%define builddir            out/headless

Summary:        chromium
Name:           chromium
# Don't bump or upgrade version of this spec
# This is a special package & needs some manual effort
Version:        131.0.6778.268
Release:        1%{?dist}
URL:            https://chromium.googlesource.com/chromium/src
Group:          System Utility
Vendor:         VMware, Inc.
Distribution:   Photon

# generated using tools/scripts/fetch-chromium-source.sh
Source0: https://github.com/chromium/chromium/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=f7f4c1533481bc318cc73314a1676af07c5be4193ba75c5480b0b50c1c99a9826b353f8e6ef7f08a72d96ab462188873def695d05edae5e469eb6857e860d187

Source1: depot_tools-d6c2e1b.tar.xz
%define sha512 depot_tools=508cd88f42309aacdf74492d0602f91eec85d0d829ecde839c72dc5bb718d61d79e20948fc2206b521a8cf55f48ac61fb62d465cbdbe6f7b2005d3e661835338

Source2: headless.gn

Source3: license.txt
%include %{SOURCE3}

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
* Wed Jan 08 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 131.0.6778.268-1
- Upgrade to v131.0.6778.268
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 125.0.6422.65-2
- Release bump for SRP compliance
* Thu May 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 125.0.6422.65-1
- Upgrade to v125.0.6422.65
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
