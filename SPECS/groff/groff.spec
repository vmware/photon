Summary:    Programs for processing and formatting text
Name:       groff
Version:    1.22.4
Release:    2%{?dist}
URL:        http://www.gnu.org/software/groff
Group:      Applications/Text
Vendor:     VMware, Inc.
Distribution:  Photon
Source0:       http://ftp.gnu.org/gnu/groff/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Provides: perl(oop_fh.pl)
Provides: perl(main_subs.pl)
Provides: perl(man.pl)
Provides: perl(subs.pl)
Requires: perl
Requires: perl-DBI
Requires: perl-DBIx-Simple
Requires: perl-DBD-SQLite
Requires: perl-File-HomeDir
%define BuildRequiresNative groff
%description
The Groff package contains programs for processing
and formatting text.
%prep
%autosetup -p1
%build
export PAGE=letter
%configure \
  --with-grofferdir=%{_datadir}/%{name}/%{version}/groffer
# make doesn't support _smp_mflags
make $(test %{_host} != %{_build} && echo "GROFFBIN=groff") \
%install
install -vdm 755 %{_defaultdocdir}/%{name}-1.22/pdf
# make doesn't support _smp_mflags
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/groff/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*/*
%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.22.4-2
- Release bump for SRP compliance
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.22.4-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.22.3-3
- Cross compilation support
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.22.3-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.22.3-1
- Updated to version 1.22.3
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.22.2-1
- Initial build. First version
