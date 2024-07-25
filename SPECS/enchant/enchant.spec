%define network_required 1
Name:           enchant
Version:        2.5.0
Release:        1%{?dist}
Summary:        A spellchecking library
Group:          Development/Languages
Vendor:         VMware, Inc.
License:        LGPLv2+
URL:            https://github.com/AbiWord/%{name}/tree/v%{version}
Distribution:   Photon

Source0: https://github.com/AbiWord/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=23a8fa5d96297f782c95d593d21badf23eb1f6d00e3eeb348cd47bcbf860c19e3ddcb4ca809f2b36b3155dd09cb6883436671de8e3f711d57add81198072cb03

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: pkg-config
BuildRequires: glib-devel
BuildRequires: gnupg
BuildRequires: groff
BuildRequires: git
BuildRequires: hunspell-devel

Requires: hunspell
Requires: glib

%description
Enchant aims to provide a simple but comprehensive abstraction for dealing with different
spell checking libraries in a consistent way.

%package        devel
Summary:        Support files necessary to compile applications with libenchant.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel

%description devel
Libraries, headers, and support files necessary to compile applications using libenchant.

%prep
%autosetup -p1

%build
./bootstrap
%configure \
    --with-hunspell \
    --with-hunspell-dir=%{_datadir}/hunspell \
    --without-hspell \
    --without-nuspell \
    --without-aspell \
    --disable-static \
    --enable-relocatable

%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/%{name}-2/%{name}_hunspell.so
%{_datadir}/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-2.pc
%{_includedir}/%{name}-2

%changelog
* Mon Feb 12 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.5.0-1
- Initial version
