Summary:	library for configuring and customizing font access.
Name:		fontconfig
Version:	2.12.1
Release:	2%{?dist}
License:	BSD/GPL
URL:		https://www.freedesktop.org/wiki/Software/fontconfig/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.freedesktop.org/software/fontconfig/release/%{name}-%{version}.tar.gz
%define sha1 fontconfig=57a5323ebdb58b3f8062a735e0927b0f5b9a7729
Patch0:		0001-Avoid-conflicts-with-integer-width-macros-from-TS-18.patch
BuildRequires:	freetype2-devel
BuildRequires:	libxml2
BuildRequires:	expat-devel
Provides:	pkgconfig(fontconfig)
%description
Fontconfig can discover new fonts when installed automatically, removing a common source of configuration problems, perform font name substitution, so that appropriate alternative fonts can be selected if fonts are missing, identify the set of fonts required to completely cover a set of languages.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
Requires:	expat-devel
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q
%patch0 -p1

%build
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=/etc \
	--localstatedir=/var \
	--docdir=/usr/share/doc/%{name}-%{version} \
	--disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
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
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.12.1-2
-   Requires expat-devel
*   Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.12.1-1
-   Initial version
