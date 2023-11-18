Name:          sbsigntools
Version:       0.9.5
Release:       2%{?dist}
Summary:       Signing utility for UEFI secure boot
License:       GPLv3+
URL:           https://git.kernel.org/pub/scm/linux/kernel/git/jejb/sbsigntools.git
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon
# upstream tarballs don't include bundled ccan
# run tools/scripts/generate-sbsigntools-tarball.sh
Source0:       %{name}-%{version}.tar.xz
%define sha512 %{name}=9c89def6e2cf248237507cc04346eb2201a047677365c7ae4f4140a405bfc243bb958f9af80a4802c0cba1bdc2c98aa5632d934c22bdadd66dcb45cd5654e8e8
# don't fetch ccan or run git from autogen.sh, already done by generate-sbsigntools-tarball.sh
Patch0:        %{name}-no-git.patch

BuildArch:     x86_64
BuildRequires: binutils-devel
BuildRequires: gnu-efi
BuildRequires: help2man
BuildRequires: util-linux-devel
BuildRequires: openssl-devel
%if 0%{?with_check}
BuildRequires: openssl
%endif
Requires:      util-linux-libs
Requires:      openssl-libs

%description
Tools to add signatures to EFI binaries and Drivers.

%prep
%autosetup -p1

%build
./autogen.sh
%configure
%make_build

%install
%make_install

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%files
%license COPYING LICENSE.GPLv3 lib/ccan/licenses/*
%doc AUTHORS ChangeLog
%{_bindir}/sbattach
%{_bindir}/sbkeysync
%{_bindir}/sbsiglist
%{_bindir}/sbsign
%{_bindir}/sbvarsign
%{_bindir}/sbverify
%{_mandir}/man1/sbattach.1.*
%{_mandir}/man1/sbkeysync.1.*
%{_mandir}/man1/sbsiglist.1.*
%{_mandir}/man1/sbsign.1.*
%{_mandir}/man1/sbvarsign.1.*
%{_mandir}/man1/sbverify.1.*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.9.5-2
- Bump version as a part of openssl upgrade
* Thu Sep 21 2023 Alexey Makhalov <amakhalov@vmware.com> 0.9.5-1
- Initial build. Based on fedora spec
  https://src.fedoraproject.org/rpms/sbsigntools/blob/rawhide/f/sbsigntools.spec
