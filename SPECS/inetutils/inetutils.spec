Summary:	Programs for basic networking
Name:		inetutils
Version:	1.9.2
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/inetutils
Group:		Applications/Communications
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/inetutils/%{name}-%{version}.tar.gz
%define sha1 inetutils=b5aa9902e3a82bfd6e75b9aa80b72111e5418447
%description
The Inetutils package contains programs for basic networking.
%prep
%setup -q
echo '#define PATH_PROCNET_DEV "/proc/net/dev"' >> ifconfig/system/linux.h 
%build
./configure \
	--prefix=%{_prefix} \
	--localstatedir=%{_var} \
	--disable-logger \
	--disable-syslogd \
	--disable-whois \
	--disable-servers \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make SUIDMODE="-o root -m 755" DESTDIR=%{buildroot} install
install -vd %{buildroot}%{_sbindir}
mv -v %{buildroot}%{_bindir}/ifconfig %{buildroot}%{_sbindir}/ifconfig
rm -rf %{buildroot}%{_infodir}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_sbindir}/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.2-3
-	GA - Bump release of all rpms
*	Wed Aug 5 2015 Divya Thaluru <dthaluru@vmware.com> 1.9.2-2
-	Packaging ifconfig in /usr/sbin directory instead of /usr/bin directory
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.9.2-1
-	Initial build.	First version
