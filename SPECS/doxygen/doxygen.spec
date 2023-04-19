Summary:        C++ tool
Name:           doxygen
Version:        1.8.20
Release:        5%{?dist}
License:        GPLv2+
URL:            https://www.doxygen.nl/download.html
Group:          Build/Tool
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://doxygen.nl/files/doxygen-%{version}.src.tar.gz
%define sha512 %{name}=65d104d25061ee59199c74c0328f59fbeaf14f0dade755187ebd43f59008adfef243d4da448b71ae04dc325b848f9bdd109eb20e6f6092f3ed19862426d060cf

BuildRequires:  cmake
BuildRequires:  python3
BuildRequires:  python3-xml
BuildRequires:  libxml2
BuildRequires:  freetype2-devel
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
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.8.20-5
- Bump version as a part of freetype2 upgrade
* Fri Feb 17 2023 Harinadh D <hdommaraju@vmware.com> 1.8.20-4
- fix make test
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.20-3
- Use cmake macros
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.8.20-2
- Bump up to compile with python 3.10
* Mon Oct 5 2020 Michelle Wang <michellew@vmware.com> 1.8.20-1
- Initial build and add this for libsigc++ build requires
