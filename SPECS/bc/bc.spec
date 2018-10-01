Summary:	precision numeric processing language
Name:		bc
Version:	1.07.1
Release:	1%{?dist}
License:	GPLv2+
URL:		https://ftp.gnu.org/gnu/bc/
Group:		System Environment/base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://ftp.gnu.org/gnu/bc/%{name}-%{version}.tar.gz
%define sha1 bc=b4475c6d66590a5911d30f9747361db47231640a
BuildRequires:  ed
%description
The Bc package contains an arbitrary precision numeric processing language.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--with-readline \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_mandir}
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags}  timetest

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%changelog
*       Mon Sep 1 2018 Sujay G <gsujay@vmware.com> 1.07.1-1
-       Bump bc version to 1.07.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.06.95-3
-	GA - Bump release of all rpms
*       Tue Aug 4 2015 Kumar Kaushik <kaushikk@vmware.com> 1.06.95-2
-       Adding the post uninstall section.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.06.95-1
-	initial version
