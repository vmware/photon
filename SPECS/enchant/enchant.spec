#Follow the below steps to create vendor enchant source
#1.Download the source file and extract it
#2.execute bootstrap file in the source
#3.tar the folder enchant-%{verson} to enchant-vendor-%{verson}.tar.gz
Name:           enchant
Version:        2.5.0
Release:        3%{?dist}
Summary:        A spellchecking library
Group:          Development/Languages
Vendor:         VMware, Inc.
URL:            https://github.com/AbiWord/%{name}/tree/v%{version}
Distribution:   Photon

Source0: https://github.com/AbiWord/%{name}/archive/refs/tags/%{name}-vendor-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
./bootstrap --skip-git --skip-po
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
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.5.0-3
- Release bump for SRP compliance
* Wed Jul 24 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 2.5.0-2
- Support for offline build
* Mon Feb 12 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.5.0-1
- Initial version
