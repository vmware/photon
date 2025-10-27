Summary:        X11 SM runtime library.
Name:           libSM
Version:        1.2.4
Release:        1%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.xz
%define sha512 %{name}=7f1d41b7b6c5dd456c49ccad7740c3ba9791a2793fa50fd94814a4164ce2e20c4a0a0ad42a87708e494ed5c23f611be6d3ccd9ef1e9add6d46ac545e2b0f6f86

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  proto
BuildRequires:  libICE-devel
Requires:       libICE

%description
The X11 Session Management runtime library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libICE-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/
%{_datadir}/*

%changelog
* Wed Oct 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2.4-1
- Initial version
