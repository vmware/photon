Summary:	Programs for compressing and decompressing files
Name:		gzip
Version:	1.6
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/gzip/%{name}-%{version}.tar.xz
%define sha1 gzip=05bd01fc90178b806e0c13f9526e2ad392084085
%description
The Gzip package contains programs for compressing and
decompressing files.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
install -vdm 755 %{buildroot}%{_bindir}
mv -v %{buildroot}/bin/{gzexe,uncompress,zcmp,zdiff,zegrep}	%{buildroot}%{_bindir}
mv -v %{buildroot}/bin/{zfgrep,zforce,zgrep,zless,zmore,znew}	%{buildroot}%{_bindir}
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
/bin/*
%{_bindir}/*
%{_mandir}/*/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6-2
-	GA - Bump release of all rpms
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.6-1
-	Initial build.	First version
