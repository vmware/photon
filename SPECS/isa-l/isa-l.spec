Summary:        Intelligent Storage Acceleration Library
Name:           isa-l
Version:        2.31.1
Release:        2%{?dist}
URL:            https://github.com/intel/isa-l
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/intel/isa-l/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=65199d054af1edc26d477883f7878f25fd4db65622aa98247069f1296c5f07b75da24f0361a6c3889ddb3168d940b508cd2f6340548a62ff3157977179fd002d

Source1: license.txt
%include %{SOURCE1}

%if 0%{?with_check}
Patch0: igzip_cli_check.sh-skip-read-write-check-for-root.patch
%endif

BuildRequires: nasm

%if 0%{?with_check}
BuildRequires: diffutils
%endif

# nasm is not available for aarch64
BuildArch: x86_64

%description
ISA-L is a collection of optimized low-level functions targeting storage applications.

%package devel
Summary: Development headers for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -p1

%build
sh ./autogen.sh

%configure --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
bash programs/igzip_cli_check.sh
%make_build tests perfs check
%endif

%clean
rm -rf %{buildroot}/*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/igzip

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}.h
%{_mandir}/*
%{_libdir}/pkgconfig/libisal.pc

%changelog
* Sat Apr 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.31.1-2
- Build for x86_64 only
* Thu Mar 20 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.31.1-1
- Initial version
