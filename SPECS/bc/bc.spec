Summary:	precision numeric processing language
Name:		bc
Version:	1.07.1
Release:	4%{?dist}
License:	GPLv2+
URL:		https://ftp.gnu.org/gnu/bc/
Group:		System Environment/base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	https://ftp.gnu.org/gnu/bc/%{name}-%{version}.tar.gz
%define sha1 bc=b4475c6d66590a5911d30f9747361db47231640a
BuildRequires:  ed
Requires: flex
Patch0:		do-not-generate-libmath-h.patch
Patch1:		pregenerated-libmath-h.patch

%description
The Bc package contains an arbitrary precision numeric processing language.

%prep
%setup -q
if [ %{_host} != %{_build} ]; then
# bc is not cross-compile friendly.
# it generates libmath.h using built in tree ./fdc tool
# which can't be run
# Use pre-generated libmath.h
%patch0 -p1
%patch1 -p1
else
# put pregenerated libmath.h to the src root
%patch1 -p2
fi

%build
autoreconf -fiv
%configure \
	--disable-silent-rules
make %{?_smp_mflags}
# check that our pregenerated libmath.h is up to date.
if [ %{_host} = %{_build} ]; then
  diff libmath.h bc/libmath.h
fi

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_mandir}
rm -rf %{buildroot}%{_infodir}

%check
cd Test
./timetest

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
*   Mon Sep 28 2020 Sujay G <gsujay@vmware.com> 1.07.1-4
-   Fix %check
*   Fri Nov 01 2019 Alexey Makhalov <amakhalov@vmware.com> 1.07.1-3
-   Cross compilation support
*   Mon Oct 14 2019 Piyush Gupta <guptapi@vmware.com> 1.07.1-2
-   Added Requires flex
*   Mon Oct 1 2018 Sujay G <gsujay@vmware.com> 1.07.1-1
-   Bump bc version to 1.07.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.06.95-3
-   GA - Bump release of all rpms
*   Tue Aug 4 2015 Kumar Kaushik <kaushikk@vmware.com> 1.06.95-2
-   Adding the post uninstall section.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.06.95-1
-   initial version
