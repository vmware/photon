Name:           glslang
Version:        11.11.0
Release:        1%{?dist}
Summary:        OpenGL and OpenGL ES shader front end and validator
License:        BSD and GPLv3+ and ASL 2.0
URL:            https://github.com/KhronosGroup/glslang
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/KhronosGroup/glslang/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=c018271d499efff03540e4572a9c2f1f752c81c87efe7f2e63c2631ac47cecfedffdcfee68eddaf9187603eaae8ccd9a3e5640a022ba9fd7d05950f7827bf8cd

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
%{_datadir}/%{name}/*
%{_libdir}/*.a
%{_libdir}/cmake/*

%changelog
* Tue Sep 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 11.11.0-1
- First build, needed for mesa-22.2.0
