Summary:	Programs for generating Makefiles
Name:		automake
Version:	1.14.1
Release:	1
License:	GPLv2+
URL:		http://www.gnu.org/software/automake/
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.xz
%description
Contains programs for generating Makefiles for use with Autoconf.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}
%check
sed -i "s:./configure:LEXLIB=/usr/lib/libfl.a &:" t/lex-{clean,depend}-cxx.sh
make -k check %{?_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_datarootdir}/aclocal/README
%{_datarootdir}/%{name}-1.14/*
%{_datarootdir}/aclocal-1.14/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.14.1-1
-	Initial build. First version
