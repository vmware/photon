Summary:        Utilities for managing the SQUASHFS filesystem
Name:           squashfs-tools
Version:        4.5.1
Release:        5%{?dist}
License:        GNU GPLv2
URL:            https://github.com/plougher/squashfs-tools/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/plougher/squashfs-tools/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=b3934ea1e26c7508110312711465644a6d9674b6b5332a7d011e191fa3c1d4b8be694214794a0f6005263d0f4e18bab96af2f7ed66a178f8e3bb3a781cd44896

BuildRequires:  which
BuildRequires:  autoconf-archive
BuildRequires:  gzip
BuildRequires:  zlib-devel

Requires: zlib
Requires: zstd-libs

%description
The squashfs-tools package contains tools for creation and extraction SQUASHFS file system.

%prep
%autosetup -p1

%build
cd %{name}
# Enable ZSTD support
sed -i 's/#ZSTD_SUPPORT = 1/ZSTD_SUPPORT = 1/' Makefile
make EXTRA_CFLAGS="-g" %{?_smp_mflags}

%install
cd %{name}
# Create relative symlinks instead of absolute
sed -i 's#ln -fs $(INSTALL_DIR)/mksquashfs#ln -fs mksquashfs#' Makefile
sed -i 's#ln -fs $(INSTALL_DIR)/unsquashfs#ln -fs unsquashfs#' Makefile
%make_install INSTALL_DIR=%{buildroot}%{_bindir} %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/mksquashfs
%{_bindir}/sqfscat
%{_bindir}/sqfstar
%{_bindir}/unsquashfs

%changelog
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.5.1-5
- Bump version as a part of zstd upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.5.1-4
- Bump version as a part of zlib upgrade
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.5.1-3
- Bump version as a part of autoconf-archive upgrade
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.5.1-2
- Bump version as a part of zstd upgrade
* Tue Mar 22 2022 Shivani Agarwal <shivania2@vmware.com> 4.5.1-1
- Fix CVE-2021-41072 CVE-2021-40153
* Tue Jan 25 2022 Alexey Makhalov <amakhalov@vmware.com> 4.5-1
- Initial build. First version
