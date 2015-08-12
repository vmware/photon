Summary:	Contains programs for manipulating text files
Name:		gawk
Version:	4.1.0
Release:	2%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/gawk
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz
%define sha1 gawk=caabca3c1a59d05807c826c45a4639b82cad612a
Provides:	/bin/gawk
Requires:	gmp
%description
The Gawk package contains programs for manipulating text files.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -v doc/{awkforai.txt,*.{eps,pdf,jpg}} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}
find %{buildroot}%{_libdir} -name '*.la' -delete
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/%{name}/*
%{_includedir}/*
%{_libexecdir}/*
%{_datarootdir}/awk/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%changelog
*	Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.0-2
-	Provide /bin/gawk.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.1.0-1
-	Initial build. First version
