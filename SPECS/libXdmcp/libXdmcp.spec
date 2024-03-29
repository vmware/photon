Summary:        X Display Manager Control Protocol library.
Name:           libXdmcp
Version:        1.1.3
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512  libXdmcp=cb1d4650f97d66e73acd2465ec7d757b9b797cce2f85e301860a44997a461837eea845ec9bd5b639ec5ca34c804f8bdd870697a5ce3f4e270b687c9ef74f25ec

BuildRequires:  proto

%description
The libXdmcp package contains a library implementing the X Display Manager Control Protocol. This is useful for allowing clients to interact with the X Display Manager.

%package        devel
Summary:        Header and development files for libXdmcp
Requires:       %{name} = %{version}-%{release}
Requires:       proto

%description    devel
libXdmcp development package.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name \*.la -delete

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libXdmcp.so.*

%files devel
%defattr(-,root,root)
%{_docdir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/libXdmcp.a
%{_libdir}/pkgconfig

%changelog
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.1.3-1
- Upgrade to 1.1.3
* Fri May 15 2015 Alexey Makhalov <amakhalov@vmware.com> 1.1.2-1
- initial version
