Summary:        C++ tool
Name:           doxygen
Version:        1.8.20
Release:        1%{?dist}
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
BuildRequires:  bison
BuildRequires:  freetype2-devel

%description
Doxygen is the de facto standard tool for generating documentation from annotated C++ sources,
but it also supports other popular programming languages such as C, Objective-C, C#, PHP, Java, Python, IDL
(Corba, Microsoft, and UNO/OpenOffice flavors), Fortran, VHDL, and to some extent D.

%prep
%autosetup -p1
mkdir -p build

%build
cd build
cmake -DLIBCLANG_BUILD_STATIC=ON \
       -DBUILD_SHARED_LIBS=OFF \
       -DLLVM_ENABLE_PIC=OFF \
       -DLLVM_BUILD_LLVM_DYLIB=OFF \
       -DLLVM_BUILD_LLVM_C_DYLIB=OFF \
       -DLLVM_ENABLE_TERMINFO=OFF \
       -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	..

%make_build

%install
cd build
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
cd build
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Mon Dec 19 2022 Harinadh D <hdommaraju@vmware.com> 1.8.20-1
- Initial release
