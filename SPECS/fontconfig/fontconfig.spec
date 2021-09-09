Summary:        library for configuring and customizing font access.
Name:           fontconfig
Version:        2.13.93
Release:        2%{?dist}
License:        BSD/GPL
URL:            https://www.freedesktop.org/wiki/Software/fontconfig/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.freedesktop.org/software/fontconfig/release/%{name}-%{version}.tar.gz
%define sha1    fontconfig=792c094e528768b37f068a2c0a35c9dbfd02793f
BuildRequires:  freetype2-devel
BuildRequires:  libxml2
BuildRequires:  expat-devel
BuildRequires:  gperf
BuildRequires:  python3
Provides:       pkgconfig(fontconfig)

%description
Fontconfig can discover new fonts when installed automatically,
removing a common source of configuration problems, perform font name substitution,
so that appropriate alternative fonts can be selected if fonts are missing,
identify the set of fonts required to completely cover a set of languages.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
Requires:	expat-devel
Requires:	freetype2-devel
%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
export PYTHON=python3
%configure \
        --disable-docs \
	--docdir=/usr/share/doc/%{name}-%{version} &&
make

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
install -v -dm755 %{buildroot}/usr/share/{man/man{1,3,5},doc/%{name}-%{version}/fontconfig-devel} &&
install -v -m644 fc-*/*.1         %{buildroot}/usr/share/man/man1 &&
install -v -m644 doc/*.3          %{buildroot}/usr/share/man/man3 &&
install -v -m644 doc/fonts-conf.5 %{buildroot}/usr/share/man/man5 &&
install -v -m644 doc/fontconfig-devel/* %{buildroot}/usr/share/doc/%{name}-%{version}/fontconfig-devel &&
install -v -m644 doc/*.{pdf,sgml,txt,html} %{buildroot}/usr/share/doc/%{name}-%{version}
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
*   Wed Aug 11 2021 Alexey Makhalov <amakhalov@vmware.com> 2.13.93-2
-   Add freetype2-devel requires for -devel subpackage.
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.13.93-1
-   Automatic Version Bump
*   Wed Sep 12 2018 Sujay G <gsujay@vmware.com> 2.13.1-1
-   Bump version to 2.13.1
*   Thu Aug 03 2017 Chang Lee <changlee@vmware.com> 2.12.1-3
-   Add a patch for run-test. This issue was introduced by freetype 2.7.1
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.12.1-2
-   Requires expat-devel
*   Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.12.1-1
-   Initial version
