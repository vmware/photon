%global _default_patch_fuzz 2
Summary:	OpenLdap-2.4.46
Name:		openldap
Version:	2.4.46
Release:	2%{?dist}
License:	OpenLDAP
URL:		http://cyrusimap.web.cmu.edu/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{name}-%{version}.tgz
%define sha1 openldap=a9ae2273eb9bdd70090dafe0d018a3132606bef6
Patch0:         openldap-2.4.40-gssapi-1.patch
Patch1:		openldap-2.4.44-consolidated-2.patch
Requires:       openssl >= 1.0.1, cyrus-sasl >= 2.1
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
BuildRequires:  cyrus-sasl >= 2.1
BuildRequires:  openssl-devel >= 1.0.1
BuildRequires:	groff
BuildRequires:	e2fsprogs-devel

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
%patch0 -p1
%patch1 -p1
%build

autoconf

sed -i '/6.0.20/ a\\t__db_version_compat' configure

CPPFLAGS="-D_REENTRANT -DLDAP_CONNECTIONLESS -D_GNU_SOURCE -D_AVL_H" \
%configure \
        --disable-static    \
        --disable-debug     \
        --enable-slapd     \
        --with-tls=openssl

make depend
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
find %{buildroot}/%{_libdir} -name '*.la' -delete
chmod 640 %{buildroot}/etc/openldap/slapd.{conf,ldif}
install -dm700 %{buildroot}/var/lib/openldap
install -dm700 %{buildroot}/etc/openldap/slapd.d
install -dm755 %{buildroot}/var/run/openldap
mkdir -p %{buildroot}/%{_lib}/tmpfiles.d
cat << EOF >> %{buildroot}/%{_lib}/tmpfiles.d/openldap.conf
d /var/run/openldap 0755 ldap ldap
EOF

%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} test

%pre
if ! getent group ldap >/dev/null; then
    /sbin/groupadd -g 83 ldap
fi
if ! getent passwd ldap >/dev/null; then
    /sbin/useradd -c "OpenLDAP Daemon Owner" -d /var/lib/openldap -u 83 -g ldap -s /bin/false ldap
fi

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    chown root:ldap /etc/openldap/slapd.{conf,ldif}
    chown -R ldap:ldap /var/run/%{name}
    chown -R ldap:ldap /var/lib/openldap
    chown -R ldap:ldap /etc/openldap/slapd.d
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    if getent passwd ldap >/dev/null; then
        /sbin/userdel ldap
    fi
    if getent group ldap >/dev/null; then
        /sbin/groupdel ldap
    fi
    rm -rf /var/run/%{name}
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_lib}/tmpfiles.d/openldap.conf
%dir %attr(0700, ldap, ldap) %{_sharedstatedir}/%{name}
%{_sharedstatedir}/%{name}/*
%{_var}/run/{%name}/
%config(noreplace) %{_sysconfdir}/openldap/slapd.conf
%config(noreplace) %{_sysconfdir}/openldap/ldap.conf
%{_sysconfdir}/openldap/*

%changelog
*   Thu Sep 06 2018 Dheeraj Shetty <dheerajs@vmware.com> 2.4.44-4
-    Enable slapd for sendmail
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.4.46-1
-   Upgrade to 2.4.46
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.44-3
-   Use standard configure macros
*   Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.44-2
-   Applied patch for CVE-2017-9287
*   Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.44-1
-   Update to 2.4.44
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.4.43-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.43-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.43-1
-   Updated to version 2.4.43
*   Fri Aug 14 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.40-2
-   Patches for CVE-2015-1545 and CVE-2015-1546.
*   Wed Oct 08 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.40-1
-   Initial build.	First version
