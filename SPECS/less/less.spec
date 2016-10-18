Summary:	Text file viewer
Name:		less
Version:	481
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.greenwoodsoftware.com/less
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%define sha1 less=58e7e62a760a9ca3636349de8e3357f7102aea1d
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
*       Tue Oct 18 2016 Anish Swaminathan <anishs@vmware.com>  481-1
-       Upgrade version to 481
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 458-2
-	GA - Bump release of all rpms
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
-	Initial build. First version
