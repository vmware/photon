Summary:        C++ tool
Name:           doxygen
Version:        1.9.5
Release:        2%{?dist}
License:        GPLv2+
URL:            https://www.doxygen.nl/download.html
Group:          Build/Tool
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://doxygen.nl/files/doxygen-%{version}.src.tar.gz
%define sha512  %{name}=4ad4c1ecd4a12220442f354b90aa56f80e78fcaf288d5e36da421437d59811ed3d429ee13717692886a55b9628ae565d40ce13c51792ccc8bba15b1e018cb651

BuildRequires:  cmake
BuildRequires:  python3
BuildRequires:  python3-xml
BuildRequires:  bison

%description
Doxygen is the de facto standard tool for generating documentation from annotated C++ sources,
but it also supports other popular programming languages such as C, Objective-C, C#, PHP, Java, Python, IDL
(Corba, Microsoft, and UNO/OpenOffice flavors), Fortran, VHDL, and to some extent D.

%prep
%autosetup -p1

%build
%cmake -DLIBCLANG_BUILD_STATIC=ON \
       -DBUILD_SHARED_LIBS=OFF \
       -DLLVM_ENABLE_PIC=OFF \
       -DLLVM_BUILD_LLVM_DYLIB=OFF \
       -DLLVM_BUILD_LLVM_C_DYLIB=OFF \
       -DLLVM_ENABLE_TERMINFO=OFF \
       -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
       ..

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
cd %{__cmake_builddir}
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.9.5-2
- Update release to compile with python 3.11
* Fri Aug 19 2022 Ajay Kaher <akaher@vmware.com> 1.9.5-1
- Version update
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.9.4-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.9.4-1
- Automatic Version Bump
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.9.1-1
- Automatic Version Bump
* Mon Oct 5 2020 Michelle Wang <michellew@vmware.com> 1.8.20-1
- Initial build and add this for libsigc++ build requires
