%global debug_package       %{nil}
%define chromium_path       %{_libdir}/%{name}-browser
%define output_dir          out/headless
%define _jobs               %(echo $(( ($(nproc)+1) / 2 )))

Summary:        chromium
Name:           chromium
# Don't bump or upgrade version of this spec
# This is a special package & needs some manual effort
Version:        150.0.7871.128
Release:        1%{?dist}
URL:            https://chromium.googlesource.com/chromium/src
Group:          System Utility
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch: x86_64

# Generated using tools/scripts/fetch-chromium-source.sh
# Contact Shreenidhi Shedi for cleanup related info.
Source0: https://github.com/chromium/chromium/archive/%{name}-%{version}.tar.xz

Source1: depot_tools-f394ab2.tar.xz

Source2: headless.gn

Source3: license.txt
%include %{SOURCE3}

Patch0: gn-tweaks.patch

BuildRequires: git
BuildRequires: bc
BuildRequires: nss-devel
BuildRequires: dbus-devel
BuildRequires: glib-devel
BuildRequires: glibc-devel
BuildRequires: nspr-devel
BuildRequires: ninja-build
BuildRequires: gperf
BuildRequires: python3
BuildRequires: python3-PyYAML

Requires: glibc
Requires: nspr
Requires: nss-libs
Requires: open-sans-fonts

%description
Chromium is an open-source browser project that aims to build a safer, faster, and more stable way for all users to experience the web.

%prep
%autosetup -a0 -a1 -p1 -n src

%build
mkdir -p %{output_dir}
cp %{SOURCE2} %{output_dir}/args.gn

py_path="$(realpath -s --relative-to=$PWD/depot_tools %{_bindir})"
echo "${py_path}" > depot_tools/python3_bin_reldir.txt

CPUS=$(nproc)
RAM_GB=$(awk '/MemTotal/ {print int($2 / 1024 / 1024)}' /proc/meminfo)

# Give 6GB RAM per link job
LINK_JOBS=$(( RAM_GB / 6 ))
(( LINK_JOBS < 1 )) && LINK_JOBS=1

# Use only 25% of available CPU cores, to avoid OOM
JOBS=$(( RAM_GB / 4 ))

if (( JOBS > CPUS )); then
  JOBS=$(( (CPUS / 2) - 1 ))
fi

if (( JOBS < 1 )); then
  JOBS=1
  HALF_JOBS=1
else
  HALF_JOBS=$(( JOBS / 2 ))
  (( HALF_JOBS < 1 )) && HALF_JOBS=1
fi

echo "concurrent_links=$LINK_JOBS" >> %{output_dir}/args.gn
sync
%{_builddir}/src/depot_tools/gn gen %{output_dir}

echo "Using $JOBS jobs ($RAM_GB GB RAM available)"

# Sometimes build breaks with OOM
for i in $(seq 1 10); do
  # Don't exceed 80% load
  LOAD=$(echo "$JOBS * 0.8 / 1" | bc)
  if ninja -C %{output_dir} headless_shell -j ${JOBS} -l ${LOAD}; then
    break
  fi
  JOBS=${HALF_JOBS}
  echo "Warning: chromium build failed, retry ($i), using $JOBS jobs" >&2
done

%install
mkdir -p %{buildroot}%{chromium_path}
cp -a  %{output_dir}/headless_lib_data.pak \
       %{output_dir}/headless_lib_strings.pak \
       %{output_dir}/headless_shell \
       %{output_dir}/libvk_swiftshader.so* \
       %{output_dir}/libvulkan.so* \
       %{output_dir}/libEGL.so* \
       %{output_dir}/libGLESv2.so* \
       %{output_dir}/vk_swiftshader_icd.json \
       %{buildroot}%{chromium_path}

> %{SOURCE0}

%files
%defattr(-,root,root)
%{chromium_path}

%changelog
* Tue Jul 21 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 150.0.7871.128-1
- Upgrade to v150.0.7871.128
* Mon May 11 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 148.0.7778.165-1
- Upgrade to v148.0.7778.165
* Sat Feb 28 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 145.0.7632.155-1
- Upgrade to v145.0.7632.155
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
