Summary:    DWARF optimization and duplicate removal tool
Name:       dwz
Version:    0.14
Release:    1%{?dist}
License:    GPLv2+ and GPLv3+
URL:        https://sourceware.org/dwz
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:     https://sourceware.org/ftp/dwz/releases/%{name}-%{version}.tar.xz
%define sha512 %{name}=62c39f79723ca99305dbb08d1d24a17699b9a84dd98c30904103da116831b1253bf1edbfb905c76fdc4d48305bd1ea0046314c5619209c40a1e624b8ae4908b1

BuildRequires: gcc
BuildRequires: gdb
BuildRequires: dejagnu
BuildRequires: make
BuildRequires: elfutils-libelf-devel

%description
The dwz package contains a program that attempts to optimize DWARF
debugging information contained in ELF shared libraries and ELF executables
for size, by replacing DWARF information representation with equivalent
smaller representation where possible and by reducing the amount of
duplication using techniques from DWARF standard appendix E - creating
DW_TAG_partial_unit compilation units (CUs) for duplicated information
and using DW_TAG_imported_unit to import it into each CU that needs it.

%prep
%autosetup -p1 -n %{name}

%build
%make_build CFLAGS='%{optflags}' \
  prefix=%{_prefix} mandir=%{_mandir} bindir=%{_bindir}

%install
rm -rf %{buildroot}
%make_install prefix=%{_prefix} mandir=%{_mandir} bindir=%{_bindir}

%check
%if 0%{?with_check}
make check %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%license COPYING COPYING3 COPYING.RUNTIME
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Fri Dec 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.14-1
- Intial version. Needed for rpm-4.17.0
