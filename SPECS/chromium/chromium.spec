%global debug_package       %{nil}
%define chromium_path       %{_libdir}/%{name}-browser
%define builddir            out/headless
%define _jobs               %(echo $(( ($(nproc)+1) / 2 )))

Summary:        chromium
Name:           chromium
# Don't bump or upgrade version of this spec
# This is a special package & needs some manual effort
Version:        142.0.7444.175
Release:        1%{?dist}
URL:            https://chromium.googlesource.com/chromium/src
Group:          System Utility
Vendor:         VMware, Inc.
Distribution:   Photon

# Generated using tools/scripts/fetch-chromium-source.sh
# Contact Shreenidhi Shedi for cleanup related info.
Source0: https://github.com/chromium/chromium/archive/%{name}-%{version}.tar.xz

Source1: depot_tools-8efa575.tar.xz

Source2: headless.gn

Source3: license.txt
%include %{SOURCE3}

Patch0: swiftshader-buildgn.patch
Patch1: build-gn.patch

BuildRequires: git
BuildRequires: nss-devel
BuildRequires: dbus-devel
BuildRequires: glib-devel
BuildRequires: glibc-devel
BuildRequires: nspr-devel
BuildRequires: ninja-build
BuildRequires: gperf
BuildRequires: python3
BuildRequires: python3-PyYAML

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
mkdir -p %{builddir}
cp %{SOURCE2} %{builddir}/args.gn

py_path="$(realpath -s --relative-to=$PWD/depot_tools %{_bindir})"
echo "${py_path}" > depot_tools/python3_bin_reldir.txt

%{_builddir}/src/depot_tools/gn gen %{builddir}

# sometimes build breaks with OOM
for i in 1 2 3; do
  if ninja -C %{builddir} headless_shell -j %{_jobs}; then
    break
  fi
  echo "Warning: chromium build failed, retry ($i)" >&2
done

%install
mkdir -p %{buildroot}%{chromium_path}
cp -a  %{builddir}/headless_lib_data.pak \
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
* Mon Dec 01 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 142.0.7444.175-1
- Upgrade to v142.0.7444.175
* Tue Sep 23 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 140.0.7339.127-1
- Upgrade to v140.0.7339.127
* Fri Jul 04 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 138.0.7204.145-1
- Upgrade to v138.0.7204.145
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
