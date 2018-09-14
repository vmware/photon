Summary:	Archiving program
Name:		tar
Version:	1.30
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/tar
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	tar/%{name}-%{version}.tar.xz
%define sha1 tar=0d442c4565f8131745a5dff1cd08f7eaa797f679
%description
Contains GNU archiving program
%prep
%setup -q
%build
FORCE_UNSAFE_CONFIGURE=1  ./configure \
	--prefix=%{_prefix} \
	--bindir=/bin \
	--disable-silent-rules
make %{?_smp_mflags}
%install
install -vdm 755 %{buildroot}%{_sbindir}
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} -C doc install-html docdir=%{_defaultdocdir}/%{name}-%{version}
install -vdm 755 %{buildroot}/usr/share/man/man1 
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make  %{?_smp_mflags} check
%files -f %{name}.lang
%defattr(-,root,root)
/bin/tar
%{_libexecdir}/rmt
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%changelog
*       Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 1.30-1
-       Update to version 1.30
*       Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.29-1
-       Update to version 1.29.
*       Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.28-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-2
-	GA - Bump release of all rpms
*	Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.28-1
-	Update to 1.28-1.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.27.1-1
-	Initial build.	First version
