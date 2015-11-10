Summary:	Reading, writing, and converting info pages
Name:		texinfo
Version:	5.2
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/texinfo/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	%{name}-%{version}.tar.xz
%define sha1 texinfo=fbbc35c5857d11d1164c8445c78b66ad6d472072
%description
The Texinfo package contains programs for reading, writing,
and converting info pages.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} TEXMF=%{_datarootdir}/texmf install-tex
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%dir %{_datarootdir}/texinfo
%{_datarootdir}/texinfo/*
%dir %{_datarootdir}/texmf
%{_datarootdir}/texmf/*
%changelog
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 5.2-3
-	Handled locale files with macro find_lang
*	Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 5.2-2
-	Removing perl-libintl package from run-time required packages
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2-1
-	Upgrade version
