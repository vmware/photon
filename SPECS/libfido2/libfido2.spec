Summary:        Command-line tools to communicate with a FIDO device over USB
Name:           libfido2
Version:        1.10.0
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/Yubico/%{name}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/Yubico/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=ba03e25d3f42f11cec74dee48c853ae35d03600f24ca06d2b751840408a132290fe22461372ae42ae31419061a63d9908c20a2c0cf3c0c9c8dbc46c34916784f

BuildRequires:  cmake
BuildRequires:  libcbor-devel
BuildRequires:  systemd-devel

Requires:  libcbor
Requires:  systemd

%description
A library provide the functionality and CLI tools to communicate with a FIDO
device over USB, and to verify attestation and assertion signatures.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
%{name}-devel contains development libraries and header files for %{name}.

%package tools
Summary:        FIDO2 CLI tools
Requires:       %{name} = %{version}-%{release}

%description -n libfido2-tools
FIDO2 CLI tools to access and configure a FIDO2 compliant authentication device.

%prep
%autosetup -p1

%build
%cmake
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -type f -name "*.a" -delete -print

%files
%defattr(-,root,root)
%doc NEWS README.adoc
%license LICENSE
%{_libdir}/libfido2.so
%{_libdir}/libfido2.so.1
%{_libdir}/libfido2.so.1.10.0

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfido2-tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri May 13 2022 Nitesh Kumar <kunitesh@vmware.com> 1.10.0-1
- Initial version
