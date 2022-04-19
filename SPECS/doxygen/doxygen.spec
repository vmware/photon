Summary:        C++ tool
Name:           doxygen
Version:        1.9.4
Release:        1%{?dist}
License:        GPLv2+
URL:            https://www.doxygen.nl/download.html
Group:          Build/Tool
Source0:        http://doxygen.nl/files/doxygen-%{version}.src.tar.gz
%define sha512  doxygen=613f17800ebd05b66b1954af4d51282a1779678e7ade6c43046fc940742a697ebdf3af8e94ac70a3422bc96def663e70eaea8c4349d192e2fe5e516c57cc345a
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  cmake
BuildRequires:  python3
BuildRequires:  python3-xml

%description
Doxygen is the de facto standard tool for generating documentation from annotated C++ sources,
but it also supports other popular programming languages such as C, Objective-C, C#, PHP, Java, Python, IDL
(Corba, Microsoft, and UNO/OpenOffice flavors), Fortran, VHDL, and to some extent D.

%prep
%autosetup

%build
mkdir build
cd build
cmake -DLIBCLANG_BUILD_STATIC=ON \
      -DBUILD_SHARED_LIBS=OFF \
      -DLLVM_ENABLE_PIC=OFF \
      -DLLVM_BUILD_LLVM_DYLIB=OFF \
      -DLLVM_BUILD_LLVM_C_DYLIB=OFF \
      -DLLVM_ENABLE_TERMINFO=OFF \
      ../
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_prefix}/local/bin/doxygen

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.9.4-1
-   Automatic Version Bump
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.9.1-1
-   Automatic Version Bump
*   Mon Oct 5 2020 Michelle Wang <michellew@vmware.com> 1.8.20-1
-   Initial build and add this for libsigc++ build requires.
