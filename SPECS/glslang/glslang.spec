Name:           glslang
Version:        11.12.0
Release:        1%{?dist}
Summary:        OpenGL and OpenGL ES shader front end and validator
License:        BSD and GPLv3+ and ASL 2.0
URL:            https://github.com/KhronosGroup/glslang
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/KhronosGroup/glslang/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=fd955f9912551668056dfe52835eef11e5dc0bf0d25b2d961a31f684adbd63bc6380759944c1921cfd63d359a58c7cc3a4a4d5eea69fa1b050f58960e5101271

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  ninja-build
BuildRequires:  python3-devel

%description
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%prep
%autosetup -p1

%build
%cmake \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install

%files
%defattr(-,root,root)
%doc README.md README-spirv-remap.txt
%{_bindir}/%{name}Validator
%{_bindir}/spirv-remap

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/
%{_libdir}/*.a
%{_libdir}/cmake/*

%changelog
* Tue Nov 1 2022 Gerrit Photon <photon-checkins@vmware.com> 11.12.0-1
- Automatic Version Bump
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 11.11.0-1
- First build, needed for mesa-22.2.0
