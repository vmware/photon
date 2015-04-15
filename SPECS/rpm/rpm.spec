Summary:	Package manager
Name:		rpm
Version:	4.11.2
Release:	1
License:	GPLv2+
URL:		http://rpm.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://rpm.org/releases/rpm-4.11.x/%{name}-%{version}.tar.bz2
Source1:	http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz
Source2:	rpm-system-configuring-scripts.tar.gz
#Requires: nspr
Requires: 	nss
Requires: 	popt
Requires: 	perl-Module-ScanDeps
Requires: 	lua
Requires:	elfutils-libelf
BuildRequires:	python2
BuildRequires:	python2-libs
BuildRequires:	python2-devel
BuildRequires:	lua-devel
BuildRequires:	popt-devel
BuildRequires:	nss-devel
BuildRequires:	elfutils-devel
%description
RPM package manager

%package devel
Requires:   python2
Summary:    Libraries and header files for rpm

%description devel
Static libraries and header files for the support library for rpm

%prep
%setup -q
%setup -q -T -D -a 1
%setup -q -T -D -a 2
mv db-5.3.28 db
%build
./autogen.sh --noconfigure
./configure \
	CPPFLAGS='-I/usr/include/nspr -I/usr/include/nss' \
        --program-prefix= \
        --prefix=%{_prefix} \
        --exec-prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_var} \
        --sharedstatedir=%{_sharedstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --disable-dependency-tracking \
       	--disable-static \
        --enable-python \
	--with-lua \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%find_lang %{name}
#	System macros and prefix
install -dm 755 %{buildroot}%{_sysconfdir}/rpm
pushd rpm-system-configuring-scripts
install -vm644 macros %{buildroot}%{_sysconfdir}/rpm/
install -vm755 brp-strip-debug-symbols %{buildroot}%{_libdir}/rpm/
install -vm755 brp-strip-unneeded %{buildroot}%{_libdir}/rpm/
popd
%post -p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}
%files -f %{name}.lang
%defattr(-,root,root)
/bin/rpm
%{_sysconfdir}/rpm/macros
%{_bindir}/*
%{_libdir}/rpm/*
%{_libdir}/rpm-plugins/*
%{_libdir}/librpmsign.so.*
%{_libdir}/librpmbuild.so.*
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%{_mandir}/fr/man8/*.gz
%{_mandir}/ja/man8/*.gz
%{_mandir}/ko/man8/*.gz
%{_mandir}/*/*.gz
%{_mandir}/pl/man1/*.gz
%{_mandir}/pl/man8/*.gz
%{_mandir}/ru/man8/*.gz
%{_mandir}/sk/man8/*.gz

%files devel
%defattr(-,root,root)
%{_libdir}/python*
%{_includedir}/*
%{_libdir}/pkgconfig/rpm.pc
%{_libdir}/librpmsign.so
%{_libdir}/librpmbuild.so
%{_libdir}/librpmio.so
%{_libdir}/librpm.so

%changelog
*	Tue Jan 13 2015 Divya Thaluru <dthaluru@vmware.com> 4.11.2-1
-	Initial build. First version
