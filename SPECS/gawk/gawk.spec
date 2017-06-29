Summary:	Contains programs for manipulating text files
Name:		gawk
Version:	4.1.3
Release:	3%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/gawk
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz
%define sha1 gawk=76b0acbbdeaa0e58466675c5faf68895eedd8306
Provides:	/bin/gawk
Provides:	awk
Requires:	mpfr
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
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 4.1.3-3
-   Bump release to built with latest toolchain
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1.3-2
-	GA - Bump release of all rpms
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 4.1.3-1
- 	Updated to version 4.1.3
*	Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.0-2
-	Provide /bin/gawk.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.1.0-1
-	Initial build. First version
