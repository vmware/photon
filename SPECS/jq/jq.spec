Summary:       jq is a lightweight and flexible command-line JSON processor.
Name:          jq
Version:       1.8.1
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/stedolan/jq
Distribution:  Photon

Source0: https://github.com/stedolan/jq/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=7eece5744008710d6098d2b945b52250184e981ed3b7a66d4e8e1d0484539a281031900fa9dda7e1004a3fcfa8b5be39814d499c66c34707b35962a365d24fde

BuildRequires: oniguruma-devel

%if 0%{?with_check}
BuildRequires: which
%endif

Requires: oniguruma

Patch0: CVE-2026-32316.patch
Patch1: CVE-2026-33947.patch
Patch2: CVE-2026-33948.patch
Patch3: CVE-2026-39956.patch
Patch4: CVE-2026-39979.patch
Patch5: CVE-2026-40164.patch

%description
jq is a lightweight and flexible command-line JSON processor.

%package devel
Summary:    Development files for jq
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for jq

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
autoreconf -fiv
%configure \
  --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

# Tests disabled for backport compatibility
# %check
# %make_build check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/libjq.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libjq.so
%{_libdir}/pkgconfig/libjq.pc
%{_includedir}/*

%changelog
* Fri Apr 17 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.8.1-2
- Fix CVE-2024-23337, CVE-2026-32316, CVE-2026-33947,
- CVE-2026-33948, CVE-2026-39956, CVE-2026-39979, CVE-2026-40164
* Thu Jul 24 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.8.1-1
- Upgrade to 1.8.1
- Fix CVE-2025-48060 and CVE-2024-23337
* Wed Jul 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6-3
- Add oniguruma support
* Tue Oct 27 2020 Dweep Advani <dadvani@vmware.com> 1.6-2
- Removed bundled oniguruma library
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6-1
- Automatic Version Bump
* Mon Nov 19 2018 Ashwin H<ashwinh@vmware.com> 1.5-4
- Add which for %check
* Tue Aug 22 2017 Chang Lee <changlee@vmware.com> 1.5-3
- Add oniguruma for %check
* Wed Jun 07 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5-2
- Fix for CVE-2015-8863 and CVE-2016-4074
* Mon May 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5-1
- Initial version
