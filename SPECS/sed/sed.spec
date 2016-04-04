Summary:	Stream editor
Name:		sed
Version:	4.2.2
Release:	1%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/sed
Group:		Applications/Editors
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/sed/%{name}-%{version}.tar.bz2
%define sha1 sed=f17ab6b1a7bcb2ad4ed125ef78948092d070de8f
%description
The Sed package contains a stream editor.

%package lang
Summary: Additional language files for sed
Group: System Environment/Programming
Requires: sed >= 4.2.2
%description lang
These are the additional language files of sed.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--htmldir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make check

%files
%defattr(-,root,root)
/bin/*
%{_mandir}/man1/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.2.2-1
-	Initial build. First version
