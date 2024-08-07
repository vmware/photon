Summary:       jq is a lightweight and flexible command-line JSON processor.
Name:          jq
Version:       1.6
Release:       3%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/stedolan/jq
Distribution:  Photon

Source0: https://github.com/stedolan/jq/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=5da71f53c325257f1f546a2520fe47828b495c953270df25ea0e37741463fdda72f0ba4d5b05b25114ec30f27a559344c2b024bacabf610759f4e3e9efadb480

BuildRequires: oniguruma-devel
%if 0%{?with_check}
BuildRequires: which
%endif

Requires: oniguruma

%description
jq is a lightweight and flexible command-line JSON processor.

%package devel
Summary:    Development files for jq
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for jq

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure \
  --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

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
%{_includedir}/*

%changelog
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
