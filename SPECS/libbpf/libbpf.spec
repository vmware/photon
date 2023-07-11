Summary:        Libbpf library
Name:           libbpf
Version:        1.1.0
Release:        2%{?dist}
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPL-2.1 OR BSD-2-Clause
URL:            https://github.com/libbpf/libbpf

Source0: https://github.com/libbpf/libbpf/archive/refs/tags/libbpf-%{version}.tar.gz
%define sha512 %{name}=751126893883c68e5472724988327e03f7f52becd472f7d6239fa838762f857e54a0347f8f824b8c32ca93b8f419310a86e1d75e3646dae72c2d2992d093b828

BuildRequires:  elfutils-libelf-devel
BuildRequires:  elfutils-devel

Requires:       elfutils-libelf
Requires:       elfutils

%description
Library for loading eBPF programs and reading and manipulating eBPF objects from user-space

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The libbpf-devel package contains libraries header files for
developing applications that use libbpf.

%prep
%autosetup -p1

%build
%make_build -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir} LIBDIR=%{_libdir} %{?_smp_mflags}

%install
%make_install -C ./src DESTDIR=%{buildroot} OBJDIR=%{_builddir} LIBDIR=%{_libdir} %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libbpf.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libbpf.so
%attr(0644,-,-) %{_includedir}/bpf/*
%attr(0644,-,-) %{_libdir}/libbpf.a
%attr(0644,-,-) %{_libdir}/pkgconfig/libbpf.pc

%changelog
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-2
- Bump version as a part of elfutils upgrade
* Fri Apr 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.0-1
- Upgrade to v1.1.0
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.0.1-2
- Bump up due to change in elfutils
* Fri Dec 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-1
- Upgrade to v1.0.1
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.0-1
- Upgrade to v1.0.0
* Mon Feb 21 2022 Mukul Sikka <msikka@vmware.com> 0.6.1-2
- Fix build error in aarch64 platform
* Wed Jan 12 2022 Susant Sahani <ssahani@vmware.com> 0.6.1-1
- Version Bump
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 0.3-1
- Automatic Version Bump
* Fri Oct 16 2020 Michelle Wang <michellew@vmware.com> 0.1.1-2
- Fix build error in aarch64 platform
* Mon Oct 05 2020 Gerrit Photon <photon-checkins@vmware.com> 0.1.1-1
- Automatic Version Bump
* Wed Sep 09 2020 Susant Sahani <ssahani@vmware.com>  0.1.0-1
- Initial release
