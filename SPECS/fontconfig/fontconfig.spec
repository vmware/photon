Summary:        library for configuring and customizing font access.
Name:           fontconfig
Version:        2.13.1
Release:        4%{?dist}
License:        BSD/GPL
URL:            https://www.freedesktop.org/wiki/Software/fontconfig/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.freedesktop.org/software/fontconfig/release/%{name}-%{version}.tar.gz
%define sha512 fontconfig=830df32e944ee21ad02a9df04787b9902af36ffc13913524acef6e38799a38c5df7a6e407cc0ff9c24455520549d53b3d85d22642a229ac654dc9269926f130b
BuildRequires:  freetype2-devel
BuildRequires:  libxml2
BuildRequires:  expat-devel
BuildRequires:  gperf
Requires:       freetype2
Provides:       pkgconfig(fontconfig)
%description
Fontconfig can discover new fonts when installed automatically, removing a common source of configuration problems, perform font name substitution, so that appropriate alternative fonts can be selected if fonts are missing, identify the set of fonts required to completely cover a set of languages.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       expat-devel
Requires:       freetype2-devel
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
%configure \
        --docdir=/usr/share/doc/%{name}-%{version} \
        --disable-static
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_datadir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%config(noreplace) %{_sysconfdir}/fonts/*
%{_defaultdocdir}/%{name}-%{version}/*

%files devel
%defattr(-,root,root)
%{_libdir}/libfontconfig.so
%{_includedir}/fontconfig/*
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
*   Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.13.1-4
-   Bump version as a part of freetype2 upgrade
*   Thu Dec 16 2021 Alexey Makhalov <amakhalov@vmware.com> 2.13.1-3
-   Fix pango -> fontconfig -> freetype2 dependency
*   Wed Aug 11 2021 Alexey Makhalov <amakhalov@vmware.com> 2.13.1-2
-   Add freetype2-devel requires for -devel subpackage.
*   Wed Sep 12 2018 Sujay G <gsujay@vmware.com> 2.13.1-1
-   Bump version to 2.13.1
*   Thu Aug 03 2017 Chang Lee <changlee@vmware.com> 2.12.1-3
-   Add a patch for run-test. This issue was introduced by freetype 2.7.1
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.12.1-2
-   Requires expat-devel
*   Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.12.1-1
-   Initial version
