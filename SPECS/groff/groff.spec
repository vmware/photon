Summary:	Programs for processing and formatting text
Name:		groff
Version:	1.22.2
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/groff
Group:		Applications/Text
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/groff/%{name}-%{version}.tar.gz
%define sha1 groff=37223941e25bb504bf54631daaabb01b147dc1d3
%description
The Groff package contains programs for processing
and formatting text.
%prep
%setup -q
%build
PAGE=letter ./configure \
	--prefix=%{_prefix} 
make %{?_smp_mflags}
%install
install -vdm 755 %{_defaultdocdir}/%{name}-1.22/pdf
make DESTDIR=%{buildroot} install
ln -sv eqn %{buildroot}%{_bindir}/geqn
ln -sv tbl %{buildroot}%{_bindir}/gtbl
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
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.22.2-1
-	Initial build. First version
