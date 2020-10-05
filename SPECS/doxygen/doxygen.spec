Summary:        C++ tool
Name:           doxygen
Version:        1.8.20
Release:        1%{?dist}
License:        GPLv2+
URL:            https://www.doxygen.nl/download.html
Group:          Build/Tool
Source0:        http://doxygen.nl/files/doxygen-%{version}.src.tar.gz
%define sha1    doxygen=606a7bb525a55a01fc7399bc50ad7589ad1d2283
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
%setup -q

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
make

%install
cd build
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_prefix}/local/bin/doxygen

%changelog
*   Mon Oct 5 2020 Michelle Wang <michellew@vmware.com> 1.8.20-1
-   Initial build and add this for libsigc++ build requires
