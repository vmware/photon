%define glibc_target_cpu %{_build}

Summary:	Main C library
Name:		glibc
Version:	2.21
Release:	1
License:	LGPLv2+
URL:		http://www.gnu.org/software/libc
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
Patch0:		glibc-2.21-fhs-1.patch
Provides:	rtld(GNU_HASH)
%description
This library provides the basic routines for allocating memory,
searching directories, opening and closing files, reading and
writing files, string handling, pattern matching, arithmetic,
and so on.

%package devel
Summary: Header files for glibc
Group: Applications/System
Requires: glibc >= 2.21
%description devel
These are the header files of glibc.

%package lang
Summary: Additional language files for glibc
Group: Applications/System
Requires: glibc >= 2.21
%description lang
These are the additional language files of glibc.

%prep
%setup -q
sed -i 's/\\$$(pwd)/`pwd`/' timezone/Makefile
%patch0 -p1
install -vdm 755 %{_builddir}/%{name}-build
# do not try to explicitly provide GLIBC_PRIVATE versioned libraries
%define __find_provides %{_builddir}/%{name}-%{version}/find_provides.sh
%define __find_requires %{_builddir}/%{name}-%{version}/find_requires.sh

# create find-provides and find-requires script in order to ignore GLIBC_PRIVATE errors
cat > find_provides.sh << _EOF
#! /bin/sh
if [ -d /tools ]; then
/tools/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
else
%{_prefix}/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
fi
exit 0
_EOF
chmod +x find_provides.sh

cat > find_requires.sh << _EOF
#! /bin/sh
if [ -d /tools ]; then
/tools/lib/rpm/find-requires %{buildroot} %{glibc_target_cpu} | grep -v GLIBC_PRIVATE
else
%{_prefix}/lib/rpm/find-requires %{buildroot} %{glibc_target_cpu} | grep -v GLIBC_PRIVATE
fi
_EOF
chmod +x find_requires.sh
#___EOF

%build
cd %{_builddir}/%{name}-build
../%{name}-%{version}/configure \
	--prefix=%{_prefix} \
	--disable-profile \
	--enable-kernel=2.6.32 \
	--enable-obsolete-rpc \
	--disable-silent-rules
make %{?_smp_mflags}
%check
cd %{_builddir}/glibc-build
make -k check > %{_topdir}/LOGS/%{name}-check.log 2>&1 || true
%install
#	Do not remove static libs
cd %{_builddir}/glibc-build
#	Create directories
make install_root=%{buildroot} install
install -vdm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -vdm 755 %{buildroot}/var/cache/nscd
install -vdm 755 %{buildroot}%{_libdir}/locale
cp -v ../%{name}-%{version}/nscd/nscd.conf %{buildroot}%{_sysconfdir}/nscd.conf
#	Install locale generation script and config file
#cp -v %{_topdir}/locale-gen.conf %{buildroot}%{_sysconfdir}
#cp -v %{_topdir}/locale-gen.sh %{buildroot}/sbin
#	Remove unwanted cruft
rm -rf %{buildroot}%{_infodir}
#	Install configuration files
cat > %{buildroot}%{_sysconfdir}/nsswitch.conf <<- "EOF"
#	Begin /etc/nsswitch.conf

	passwd: files
	group: files
	shadow: files

	hosts: files dns
	networks: files

	protocols: files
	services: files
	ethers: files
	rpc: files
#	End /etc/nsswitch.conf
EOF
cat > %{buildroot}%{_sysconfdir}/ld.so.conf <<- "EOF"
#	Begin /etc/ld.so.conf
	/usr/local/lib
	/opt/lib
	include /etc/ld.so.conf.d/*.conf
EOF
%post
printf "Creating ldconfig cache\n";/sbin/ldconfig
#printf "Creating locale files\n";/sbin/locale-gen.sh
%files
%defattr(-,root,root)
%dir %{_localstatedir}/cache/nscd
%dir %{_libdir}/locale
%{_sysconfdir}/*
%ifarch x86_64
%{_lib64}/*
%{_lib64dir}/*
%else
%{_lib}/*
%endif
/sbin/*
%{_bindir}/*
%{_libexecdir}/*
%{_sbindir}/*
%{_datadir}/i18n/charmaps/*.gz
%{_datadir}/i18n/locales/*
%{_localstatedir}/lib/nss_db/Makefile

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files lang
%defattr(-,root,root)
%lang(be) %{_datarootdir}/locale/be/LC_MESSAGES/libc.mo
%lang(bg) %{_datarootdir}/locale/bg/LC_MESSAGES/libc.mo
%lang(ca) %{_datarootdir}/locale/ca/LC_MESSAGES/libc.mo
%lang(cs) %{_datarootdir}/locale/cs/LC_MESSAGES/libc.mo
%lang(da) %{_datarootdir}/locale/da/LC_MESSAGES/libc.mo
%lang(de) %{_datarootdir}/locale/de/LC_MESSAGES/libc.mo
%lang(el) %{_datarootdir}/locale/el/LC_MESSAGES/libc.mo
%lang(en_GB) %{_datarootdir}/locale/en_GB/LC_MESSAGES/libc.mo
%lang(eo) %{_datarootdir}/locale/eo/LC_MESSAGES/libc.mo
%lang(es) %{_datarootdir}/locale/es/LC_MESSAGES/libc.mo
%lang(fi) %{_datarootdir}/locale/fi/LC_MESSAGES/libc.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/libc.mo
%lang(gl) %{_datarootdir}/locale/gl/LC_MESSAGES/libc.mo
%lang(hr) %{_datarootdir}/locale/hr/LC_MESSAGES/libc.mo
%lang(hu) %{_datarootdir}/locale/hu/LC_MESSAGES/libc.mo
%lang(ia) %{_datarootdir}/locale/ia/LC_MESSAGES/libc.mo
%lang(id) %{_datarootdir}/locale/id/LC_MESSAGES/libc.mo
%lang(it) %{_datarootdir}/locale/it/LC_MESSAGES/libc.mo
%lang(ja) %{_datarootdir}/locale/ja/LC_MESSAGES/libc.mo
%lang(ko) %{_datarootdir}/locale/ko/LC_MESSAGES/libc.mo
%{_datarootdir}/locale/locale.alias
%lang(lt) %{_datarootdir}/locale/lt/LC_MESSAGES/libc.mo
%lang(nb) %{_datarootdir}/locale/nb/LC_MESSAGES/libc.mo
%lang(nl) %{_datarootdir}/locale/nl/LC_MESSAGES/libc.mo
%lang(pl) %{_datarootdir}/locale/pl/LC_MESSAGES/libc.mo
%lang(pt_BR) %{_datarootdir}/locale/pt_BR/LC_MESSAGES/libc.mo
%lang(ru) %{_datarootdir}/locale/ru/LC_MESSAGES/libc.mo
%lang(rw) %{_datarootdir}/locale/rw/LC_MESSAGES/libc.mo
%lang(sk) %{_datarootdir}/locale/sk/LC_MESSAGES/libc.mo
%lang(sl) %{_datarootdir}/locale/sl/LC_MESSAGES/libc.mo
%lang(sv) %{_datarootdir}/locale/sv/LC_MESSAGES/libc.mo
%lang(tr) %{_datarootdir}/locale/tr/LC_MESSAGES/libc.mo
%lang(uk) %{_datarootdir}/locale/uk/LC_MESSAGES/libc.mo
%lang(vi) %{_datarootdir}/locale/vi/LC_MESSAGES/libc.mo
%lang(zh_CN) %{_datarootdir}/locale/zh_CN/LC_MESSAGES/libc.mo
%lang(zh_TW) %{_datarootdir}/locale/zh_TW/LC_MESSAGES/libc.mo

%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.19-1
-	Initial build. First version
