Summary:	Programs for processing and formatting text
Name:		groff
Version:	1.22.3
Release:	3%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/groff
Group:		Applications/Text
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/groff/%{name}-%{version}.tar.gz
%define sha1 groff=61a6808ea1ef715df9fa8e9b424e1f6b9fa8c091
Provides:	perl(oop_fh.pl)
Provides:	perl(main_subs.pl)
Provides:   perl(man.pl)
Provides:   perl(subs.pl)
Requires: perl >= 5.28.0
Requires: perl-DBI
Requires: perl-DBIx-Simple
Requires: perl-DBD-SQLite
Requires: perl-File-HomeDir
%description
The Groff package contains programs for processing
and formatting text.
%prep
%setup -q
%build
PAGE=letter %configure \
	--with-grofferdir=%{_datadir}/%{name}/%{version}/groffer
make
%install
install -vdm 755 %{_defaultdocdir}/%{name}-1.22/pdf
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/groff/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*/*
%changelog
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.22.3-3
-   Consuming perl version upgrade of 5.28.0
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.22.3-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.22.3-1
-   Updated to version 1.22.3
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.22.2-1
-   Initial build. First version
