%global build_if %{photon_subrelease} >= 91
%define debug_package %{nil}

Name:           7zip
Version:        26.01
Release:        2%{?dist}
Summary:        A file archiver
URL:            https://7-zip.org
Vendor:         VMware, Inc.
Group:          Applications/System
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# Taken from Fedora
Patch0: 7z-dont-echo-password.patch
Patch1: 7zip-find-so-in-libexec.patch

BuildRequires: build-essential

Requires: libstdc++
Requires: glibc-libs
Requires: libgcc

Obsoletes: zip
Obsoletes: unzip

%description
7-Zip is a file archiver with a high compression ratio. The main features
of 7-Zip are:

* High compression ratio in 7z format with LZMA and LZMA2 compression
* Supported formats:
  * Packing / unpacking: 7z, XZ, BZIP2, GZIP, TAR, ZIP and WIM
  * Unpacking only: AR, ARJ, CAB, CHM, CPIO, CramFS, DMG, EXT, FAT,
    GPT, HFS, IHEX, ISO, LZH, LZMA, MBR, MSI, NSIS, NTFS, QCOW2,
    RPM, SquashFS, UDF, UEFI, VDI, VHD, VMDK, WIM, XAR and Z.
* For ZIP and GZIP formats, 7-Zip provides a compression ratio that is
  2-10 % better than the ratio provided by PKZip and WinZip
* Strong AES-256 encryption in 7z and ZIP formats
* Powerful command line version}

%prep
%autosetup -p1

%build
_platform_flags=()
CARCH="$(uname -m)"

case $CARCH in
  x86_64)
    _platform_flags=(PLATFORM=x64 IS_X64=1)
  ;;
  aarch64)
    _platform_flags=(PLATFORM=arm64 IS_ARM64=1)
  ;;
  *)
  echo "ERROR: unsupported arch $CARCH" >&2
  exit 1
  ;;
esac

for component in Bundles/{Alone,Alone2,Alone7z,Format7zF} UI/Console; do
  %make_build -C CPP/%{name}/$component -f ../../cmpl_gcc.mak "${_platform_flags[@]}"
done

%install
install -Dt "%{buildroot}%{_libexecdir}/%{name}" \
  CPP/%{name}/Bundles/Alone/b/g/7za \
  CPP/%{name}/Bundles/Alone2/b/g/7zz \
  CPP/%{name}/Bundles/Alone7z/b/g/7zr \
  CPP/%{name}/Bundles/Format7zF/b/g/7z.so \
  CPP/%{name}/UI/Console/b/g/7z

for _prog in 7za 7zr 7z 7zz; do
  printf '#!/bin/bash\nexec %{_libexecdir}/%{name}/%s "$@"\n' "$_prog" \
   | install -D /dev/stdin "%{buildroot}%{_bindir}/$_prog"
done

%files
%defattr(-,root,root)
%{_libexecdir}/%{name}/7z
%{_libexecdir}/%{name}/7za
%{_libexecdir}/%{name}/7zr
%{_libexecdir}/%{name}/7zz
%{_libexecdir}/%{name}/7z.so
%{_bindir}/7z
%{_bindir}/7za
%{_bindir}/7zr
%{_bindir}/7zz

%changelog
* Mon Jun 08 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.01-2
- Disable debuginfo package
* Mon Jun 08 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 26.01-1
- Initial version.
