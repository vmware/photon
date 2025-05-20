Name:           hunspell
Version:        1.7.2
Release:        2%{?dist}
Summary:        A spell checker and morphological analyzer library
Group:          Development/Languages
Vendor:         VMware, Inc.
URL:            https://github.com/hunspell/hunspell
Distribution:   Photon

Source0: https://github.com/hunspell/hunspell/releases/download/v%{version}/hunspell-%{version}.tar.gz

# While upgrading this package, please generate the tarball using the
# fetch-dictionaries-files.sh script provided in tools/scripts dir.
# Note: The dictionary files for en_US and en_GB has been taken from
# URL: https://github.com/wooorm/dictionaries
Source1: dictionaries-1.0.tar.gz

Source2: license.txt
%include %{SOURCE2}

BuildRequires: perl
BuildRequires: libtool
BuildRequires: gettext-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: texinfo
BuildRequires: pkg-config
BuildRequires: ncurses-devel

Requires: perl-libintl
Requires: gettext
Requires: ncurses

%description
Hunspell is a free spell checker and morphological analyzer library and command-line tool,
licensed under LGPL/GPL/MPL tri-license.

%package        devel
Summary:        Support files necessary to compile applications with hunspell.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Libraries, headers, and support files necessary to compile applications using hunspell.

%prep
%autosetup -a0 -a1 -p1

%build
autoreconf -vfi

%configure \
    --enable-static=no \
    --with-ncurses=yes

%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_datadir}/%{name}
install -m0644 dictionaries/*.aff %{buildroot}%{_datadir}/%{name}
install -m0644 dictionaries/*.dic %{buildroot}%{_datadir}/%{name}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.7.2-2
- Release bump for SRP compliance
* Mon Feb 12 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.7.2-1
- Initial version, required by enchant
