%global _default_patch_fuzz 2
Summary:	OpenLdap-2.4.40
Name:		openldap
Version:	2.4.40
Release:	1
License:	OpenLDAP
URL:		http://cyrusimap.web.cmu.edu/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/openldap-2.4.40.tgz
Source1:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20140919.tar.bz2
Patch0:		openldap-2.4.40-blfs_paths-1.patch
Patch1:		openldap-2.4.40-symbol_versions-1.patch
Patch2:		openldap-2.4.40-gssapi-1.patch
Requires:       openssl >= 1.0.1, cyrus-sasl >= 2.1
BuildRequires:  cyrus-sasl >= 2.1
BuildRequires:  openssl-devel >= 1.0.1
BuildRequires:	groff
%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.
%prep
%setup -q
%patch2 -p1
%patch1 -p1
%patch0 -p1 
tar xf %{SOURCE1}
%build

autoconf

sed -i '/6.0.20/ a\\t__db_version_compat' configure

CPPFLAGS="-D_REENTRANT -DLDAP_CONNECTIONLESS -D_GNU_SOURCE -D_AVL_H" \
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
        --sysconfdir=/etc   \
        --disable-static    \
        --disable-debug     \
        --disable-slapd     \
        --with-tls=openssl

make depend
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
/etc/openldap/*

%changelog
*	Wed Oct 08 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.40-1
-	Initial build.	First version
