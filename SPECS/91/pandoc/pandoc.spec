%global build_if %{photon_subrelease} <= 91

%global debug_package %{nil}

Summary:        Conversion between markup formats
Name:           pandoc-bin
Version:        2.19.2
Release:        5.1%{?dist}
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

Source1: license.txt
%include %{SOURCE1}

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
* Fri Mar 27 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.19.2-5.1
- Bump after moving to SPECS/91
* Sun Aug 03 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 2.19.2-5
- Bump up release to rescan licenses
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.19.2-4
- Release bump for SRP compliance
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 2.19.2-3
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.19.2-2
- Release bump for SRP compliance
* Tue Nov 1 2022 Gerrit Photon <photon-checkins@vmware.com> 2.19.2-1
- Automatic Version Bump
* Sun Dec 26 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.17.1.1-1
- Initial version, needed for rpm-4.17.0
