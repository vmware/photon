Summary:	Gperf-3.0.4
Name:		gperf
Version:	3.1
Release:	2%{?dist}
License:	GPLv3+
URL:		http://freedesktop.org/wiki/Software/%{name}l/
Source0:	http://ftp.gnu.org/gnu/gperf/%{name}-%{version}.tar.gz
%define sha1 gperf=e3c0618c2d2e5586eda9498c867d5e4858a3b0e2
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon

%description
Gperf generates a perfect hash function from a key set.

%prep
%setup -q

%build
%configure \
	--docdir=%{_defaultdocdir}/%{name}-%{version}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -v -m644 doc/gperf.{dvi,ps,pdf} %{buildroot}/%{_docdir}/%{name}-%{version}
pushd  %{buildroot}/usr/share/info &&
  for FILENAME in *; do
    install-info $FILENAME %{name}-%{version} 2>/dev/null
  done &&
popd

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*
%{_mandir}/man1/*
%{_datadir}/info/*
%{_bindir}/*

%changelog
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 3.1-2
-   Cross compilation support
*   Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> 3.1-1
-   Updated to version 3.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.4-2
-   GA - Bump release of all rpms
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.4-1
-   Initial build. First version
