Summary:        Utilities for managing the SQUASHFS filesystem
Name:           squashfs-tools
Version:        4.5.1
Release:        1%{?dist}
License:        GNU GPLv2
URL:            https://github.com/plougher/squashfs-tools/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/plougher/squashfs-tools/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha1    squashfs-tools=3dc0a4d88b0a40f1537cea5e50371c1be0bb590f
BuildRequires:  which
BuildRequires:  autoconf-archive
BuildRequires:  gzip
BuildRequires:  zlib-devel zstd-devel
Requires:       zlib zstd-libs

%description
The squashfs-tools package contains tools for creation and extraction SQUASHFS file system.

%prep
%autosetup

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
make INSTALL_DIR=%{buildroot}%{_bindir} %{?_smp_mflags} install

%files
%defattr(-,root,root)
%{_bindir}/mksquashfs
%{_bindir}/sqfscat
%{_bindir}/sqfstar
%{_bindir}/unsquashfs

%changelog
* Tue Mar 22 2022 Shivani Agarwal <shivania2@vmware.com> 4.5.1-1
- Fix CVE-2021-41072 CVE-2021-40153
* Tue Jan 25 2022 Alexey Makhalov <amakhalov@vmware.com> 4.5-1
- Initial build. First version
