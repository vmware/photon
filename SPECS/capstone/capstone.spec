Summary:        Disassembly framework
Name:           capstone
Version:        4.0.2
Release:        2%{?dist}
URL:            https://github.com/aquynh/capstone
Source0:        https://github.com/aquynh/%{name}/archive/%{name}-%{version}.tar.gz
%define sha512  %{name}=7f93534517307b737422a8825b66b2a1f3e1cca2049465d60ab12595940154aaf843ba40ed348fce58de58b990c19a0caef289060eb72898cb008a88c470970e

Source1: license.txt
%include %{SOURCE1}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
%description
Capstone is a disassembly framework with the target of becoming the ultimate disasm engine for binary analysis and reversing in the security community.

%package devel
Summary:        Development libraries and header files for capstone
Requires:       %{name} = %{version}-%{release}
%description devel
The package contains libraries and header files for
developing applications that use capstone.

%prep
%autosetup

%build
CAPSTONE_ARCHS="x86_64 aarch64" ./make.sh

%install
DESTDIR=%{buildroot} ./make.sh install
rm %{buildroot}/%{_libdir}/libcapstone.a

%check
make %{?_smp_mflags} test_basic test_detail test_iter test_skipdata test_arm64 test_x86 test_basic.static test_detail.static test_iter.static test_skipdata.static test_arm64.static test_x86.static

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/cstool
%{_libdir}/libcapstone.so.4

%files devel
%defattr(-,root,root)
%dir %{_includedir}/capstone
%{_includedir}/capstone/*
%{_libdir}/libcapstone.so
%{_libdir}/pkgconfig/capstone.pc

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 4.0.2-2
- Release bump for SRP compliance
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.2-1
- Automatic Version Bump
* Tue Nov 19 2019 Alexey Makhalov <amakhalov@vmware.com> 4.0.1-1
- Initial build. First version
