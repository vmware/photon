Summary:        Interface to the X Window System protocol.
Name:           libxcb
Version:        1.15
Release:        2%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.gz
%define sha512  libxcb=4099899c37fdda62a9a0883863ee9e50b5072e8f396ba6f4594965d9f1743fb6ea991974a99974c6f39bac14ce9aad5669fa633ac1ad2390280d613cc66eb00e

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  libXau-devel
BuildRequires:  xcb-proto
BuildRequires:  libXdmcp-devel
BuildRequires:  python3-xml

Requires:       libXdmcp
Requires:       libXau

Provides:       pkgconfig(x11-xcb)

%description
The libxcb package provides an interface to the X Window System protocol, which replaces the current Xlib interface. Xlib can also use XCB as a transport layer, allowing software to make requests and receive responses with both.

%package        devel
Summary:        Header and development files for libxcb
Requires:       %{name} = %{version}-%{release}
Requires:       libXau-devel
Requires:       xcb-proto
Requires:       libXdmcp-devel

%description    devel
The libxcb-devel package contains libraries and header files for developing
applications that use libxcb.

%prep
%autosetup -p1

%build
sed -i "s/pthread-stubs//" configure
%configure --enable-xinput \
           --docdir=%{_datadir}/doc/libxcb-1.11

%make_build

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check |& tee %{_specdir}/%{name}-check-log
%endif

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name \*.la -delete

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_datadir}/*
%{_includedir}/*
%{_libdir}/*.a*
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.15-2
- Release bump for SRP compliance
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.15-1
- Upgrade to 1.15
* Mon May 18 2015 Alexey Makhalov <amakhalov@vmware.com> 1.11-1
- initial version
