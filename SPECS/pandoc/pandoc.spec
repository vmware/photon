%global debug_package %{nil}

Summary:        Conversion between markup formats
Name:           pandoc-bin
Version:        2.17.1.1
Release:        1%{?dist}
License:        GPLv2+
URL:            https://github.com/jgm/pandoc
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

# To package the source:
# -> Goto https://github.com/jgm/pandoc/releases/
# -> Get the desired version tar archives for amd64 & aarch64
# -> Unpack them and put them in a single tar archive
# Example: for v2.17.1.1
# mkdir -p pandoc-2.17.1.1 && cd pandoc-2.17.1.1
# Download amd64 & aarch64 tar archives
# tar xf pandoc-2.17.1.1-linux-arm64.tar.gz && mv pandoc-2.17.1.1 aarch64
# tar xf pandoc-2.17.1.1-linux-amd64.tar.gz && mv pandoc-2.17.1.1 amd64
# cd .. && tar cJf pandoc-2.17.1.1.tar.xz pandoc-2.17.1.1
Source0:        pandoc-%{version}.tar.xz
%define sha512  pandoc=e27e93138c3b6258a4849df23d8c0c6439e8efd26166922300ff5401f5bf68d481e6bba452c51ca24c8dbbce5894c23bde9aeef9db571078454e8caf07d3becc

%description
Pandoc - executable only, without Haskell depends/makedepends

%package devel
Summary: Pandoc man pages

%description    devel
Contains Pandoc man pages

%prep

%autosetup -p1 -n pandoc-%{version}

%build

%install
mkdir -p %{buildroot}%{_mandir} %{buildroot}%{_bindir}
pushd "%{_arch}"
mv share/man/* %{buildroot}%{_mandir}
mv bin/pandoc %{buildroot}%{_bindir}
popd

%files
%defattr(-,root,root)
%{_bindir}/pandoc

%files devel
%defattr(-,root,root)
%{_mandir}/*

%changelog
* Sun Dec 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.17.1.1-1
- Initial version, needed for rpm-4.17.0
