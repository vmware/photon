Summary:    fuse filesystem to access remote ssh servers
Name:       sshfs
Version:    3.7.0
Release:    5%{?dist}
License:    GPLv2
Url:        https://github.com/libfuse/sshfs
Group:      Filesystemd tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/libfuse/sshfs/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=8ce33e6f29a8d372a43a52c2e3cb3a08419bf9943d3a20425e9c8bec4ec6ec419c32bb5e5a86c67e1f8593505645a1d1d41ce638a35bb0aa24db0264812f8a40

Requires:   fuse >= 2.3
Requires:   fuse3 >= 3.0.0
Requires:   glib >= 2.68.4

BuildRequires:  fuse3-devel >= 3.0.0
BuildRequires:  meson >= 0.38.0

%description
This is a usermode fuse client to mount remote filesystems through SSH File Transfer Protocol.

%prep
%autosetup -p1 -n sshfs-sshfs-%{version}

%build
mkdir build && cd build
meson --prefix=%{_prefix} .. && ninja

%install
cd build
DESTDIR=%{buildroot} ninja install

%check
%if 0%{?with_check}
#cd build && pytest test
%endif

%files
%defattr(-, root, root)
%{_bindir}/*
%{_sbindir}/*
%exclude %dir %{_libdir}
%exclude %dir %{_prefix}/src

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.7.0-5
- Bump version as a part of meson upgrade
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.7.0-4
- Bump version as part of glib upgrade
* Thu Mar 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.7.0-3
- Exclude debug symbols properly
* Tue Mar 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.7.0-2
- Remove meson from Requires
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.7.0-1
- Automatic Version Bump
* Mon Oct 08 2018 Srinidhi Rao <srinidhir@vmware.com> 3.5.0-1
- Updated to version 3.5.0
* Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 2.9-1
- Updated to version 2.9
* Fri Nov 04 2016 Sharath George <sharathg@vmware.com> 2.8-1
- Initial commit.
