Summary:	cpio-2.11
Name:		cpio
Version:	2.11
Release:	1
License:	GPLv3+
URL:		http://www.gnu.org/software/cpio/
Group:		System Environment/System utilities
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/pub/gnu/cpio/%{name}-%{version}.tar.bz2
%description
The cpio package contains tools for archiving.
%prep
%setup -q
%build
sed -i -e '/gets is a/d' gnu/stdio.in.h
./configure \
	--prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --enable-mt   \
        --with-rmt=/usr/libexec/rmt
make %{?_smp_mflags}
makeinfo --html            -o doc/html      doc/cpio.texi
makeinfo --html --no-split -o doc/cpio.html doc/cpio.texi
makeinfo --plaintext       -o doc/cpio.txt  doc/cpio.texi
%check
make -k check %{?_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%install
make DESTDIR=%{buildroot} install
install -v -m755 -d %{buildroot}/%{_docdir}/%{name}-%{version}/html
install -v -m644    doc/html/* %{buildroot}/%{_docdir}/%{name}-%{version}/html
install -v -m644    doc/cpio.{html,txt} %{buildroot}/%{_docdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_datarootdir}/locale/*
%{_mandir}/man1/*
%{_docdir}/%{name}-%{version}/*
%changelog
*	Tue Nov 04 2014 Divya Thaluru <dthaluru@vmware.com> 2.11-1
-	Initial build. First version
