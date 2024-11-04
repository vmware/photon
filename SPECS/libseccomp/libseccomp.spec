Summary:       Enhanced seccomp library
Name:          libseccomp
Version:       2.5.4
Release:       3%{?dist}
Group:         System Environment/Libraries
Url:           https://github.com/seccomp/libseccomp/wiki
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=6b07e25e63fed380bfe1dc89b9336b68cc1828c8413b6574f191450b92503a9f0a904bb0d1b7c129de976cc421b4d3f28e19d953e2591fdcbf126f4755ec7aad

Source1: license.txt
%include %{SOURCE1}

BuildRequires: which
BuildRequires: gperf

%if 0%{?with_check}
BuildRequires: which
%endif

%description
The libseccomp library provides an easy to use, platform independent, interface
to the Linux Kernel syscall filtering mechanism: seccomp. The libseccomp API
is designed to abstract away the underlying BPF based syscall filter language
and present a more conventional function-call based filtering interface that
should be familiar to, and easily adopted by application developers.

%package       devel
Summary:       Development files used to build applications with libseccomp support
Group:         Development/Libraries
Provides:      pkgconfig(libseccomp)
Requires:      %{name} = %{version}-%{release}

%description   devel
The libseccomp-devel package contains the libraries and header files
needed for developing secure applications.

%prep
%autosetup -p1

%build
./autogen.sh
%configure
%make_build

%install
%make_install %{?_smp_mflags}

rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE
%doc CREDITS
%doc README.md
%{_libdir}/libseccomp.so.*

%files devel
%{_includedir}/seccomp.h
%{_includedir}/seccomp-syscalls.h
%{_libdir}/libseccomp.so
%{_libdir}/libseccomp.a
%{_libdir}/pkgconfig/libseccomp.pc
%{_bindir}/scmp_sys_resolver
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.5.4-3
- Release bump for SRP compliance
* Mon Aug 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.5.4-2
- Remove .la files
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.5.4-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.5.1-1
- Automatic Version Bump
* Wed Sep 23 2020 Michelle Wang <michellew@vmware.com> 2.5.0-2
- Fix make check for libseccomp
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.0-1
- Automatic Version Bump
* Thu May 7 2020 Susant Sahani <ssahani@vmware.com> 2.4.3-1
- Updated to version 2.4.3.
* Wed Jan 9 2019 Michelle Wang <michellew@vmware.com> 2.3.3-2
- Fix make check for libseccomp.
* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 2.3.3-1
- Updated to version 2.3.3.
* Tue Apr 11 2017 Harish Udaiya KUmar <hudaiyakumar@vmware.com> 2.3.2-1
- Updated to version 2.3.2.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.3-2
- GA - Bump release of all rpms.
* Sat Jan 16 2016 Fabio Rapposelli <fabio@vmware.com> - 2.2.3-1
- First release of the package.
