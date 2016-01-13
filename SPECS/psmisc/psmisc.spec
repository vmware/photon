Summary:	Displays information about running processes
Name:		psmisc
Version:	22.21
Release:	1%{?dist}
License:	GPLv2+
URL:		http://psmisc.sourceforge.net/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://prdownloads.sourceforge.net/psmisc/%{name}-%{version}.tar.gz
%define sha1 psmisc=09fabbef4539b58b6b8738a73da3d21d5daa1a58
BuildRequires:	ncurses-devel
Requires:	ncurses
%description
The Psmisc package contains programs for displaying information
about running processes.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/fuser   %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/killall %{buildroot}/bin
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
%{_bindir}/*
%{_mandir}/*/*
%changelog
*	Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 22.21-1
-	Update version
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 22.20-1
-	Initial build. First version
