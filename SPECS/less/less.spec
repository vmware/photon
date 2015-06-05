Summary:	Text file viewer
Name:		less
Version:	458
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.greenwoodsoftware.com/less
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
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
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
-	Initial build. First version
