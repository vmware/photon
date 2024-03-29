Name:          dwarves
Summary:       Debugging Information Manipulation Tools (pahole & friends)
Version:       1.24
Release:       3%{?dist}
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon
License:       GPLv2
URL:           https://github.com/acmel/dwarves
Source0:       http://fedorapeople.org/~acme/dwarves/%{name}-%{version}.tar.xz
%define sha512 %{name}-%{version}=3cdca183cf68ec46fd9a0301ae4a8a30b23a8139c65ffba64ae11f85f9e942f7341dca6f88a4a3b49f32bfd880927193a80fa011726e4a33d3e5a1a146326c06
Patch0: 0001-pahole-Support-lang-lang_exclude-asm.patch
Patch1: 0001-btf_encoder-Add-extra-debug-info-for-unsupported-DWA.patch
Patch2: 0001-btf_encoder-Store-the-CU-being-processed-to-avoid-ch.patch
Patch3: 0001-core-Record-if-a-CU-has-a-DW_TAG_unspecified_type.patch
Patch4: 0001-btf_encoder-Encode-DW_TAG_unspecified_type-returning.patch
Patch5: 0001-dwarves-Zero-initialize-struct-cu-in-cu__new-to-prev.patch
BuildRequires: gcc
BuildRequires: cmake
BuildRequires: zlib-devel
BuildRequires: elfutils-devel
Requires:      elfutils
Requires:      elfutils-libelf
Requires:      zlib
Requires:      %{name}-libs = %{version}-%{release}

%description
dwarves is a set of tools that use the debugging information inserted in
ELF binaries by compilers such as GCC, used by well known debuggers such as
GDB, and more recent ones such as systemtap.

Utilities in the dwarves suite include pahole, that can be used to find
alignment holes in structs and classes in languages such as C, C++, but not
limited to these.

It also extracts other information such as CPU cacheline alignment, helping
pack those structures to achieve more cache hits.

These tools can also be used to encode and read the BTF type information format
used with the Linux kernel bpf syscall, using 'pahole -J' and 'pahole -F btf'.

A diff like tool, codiff can be used to compare the effects changes in source
code generate on the resulting binaries.

Another tool is pfunct, that can be used to find all sorts of information about
functions, inlines, decisions made by the compiler about inlining, etc.

One example of pfunct usage is in the fullcircle tool, a shell that drivers
pfunct to generate compileable code out of a .o file and then build it using
gcc, with the same compiler flags, and then use codiff to make sure the
original .o file and the new one generated from debug info produces the same
debug info.

Pahole also can be used to use all this type information to pretty print raw data
according to command line directions.

Headers can have its data format described from debugging info and offsets from
it can be used to further format a number of records.

The btfdiff utility compares the output of pahole from BTF and DWARF to make
sure they produce the same results.

%package        libs
Summary:        Debugging information processing library

%description    libs
Debugging information processing library.

%package        devel
Summary:        Debugging information library development files
Requires:       %{name} = %{version}-%{release}

%description    devel
Debugging information processing library development files.

%prep
%autosetup -p1

%build
%cmake -DCMAKE_BUILD_TYPE=Debug .
%cmake_build

%install
%cmake_install

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_datadir}/*

%changelog
*  Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.24-3
-  Bump version as a part of elfutils upgrade
*  Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.24-2
-  Bump version as a part of zlib upgrade
*  Fri Apr 07 2023 Srish Srinivasan <ssrish@vmware.com> 1.24-1
-  Initial build.
