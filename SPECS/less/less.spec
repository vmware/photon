Summary:	Text file viewer
Name:		less
Version:	458
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.greenwoodsoftware.com/less
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%define sha1 less=d5b07180d3dad327ccc8bc66818a31577e8710a2
BuildRequires:	ncurses-devel
Requires:	ncurses
%description
The Less package contains a text file viewer
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 458-2
-	GA - Bump release of all rpms
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
-	Initial build. First version
