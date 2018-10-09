Summary:	Contains programs for manipulating text files
Name:		gawk
Version:	4.2.1
Release:	1%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/gawk
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz
%define sha1 gawk=71fc3595865ea6ea859587cbbb35cbf9aeb39d2d
Provides:	/bin/awk
Provides:	/bin/gawk
Provides:	awk
Requires:	mpfr
Requires:	gmp
Requires:	readline >= 7.0
%description
The Gawk package contains programs for manipulating text files.
%prep
%setup -q
%build
%configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir } \
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
sed -i 's/ pty1 / /' test/Makefile
make %{?_smp_mflags} check

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
%{_sysconfdir}/profile.d/gawk.csh
%{_sysconfdir}/profile.d/gawk.sh
%changelog
*   Mon Sep 17 2018 Sujay G <gsujay@vmware.com> 4.2.1-1
-   Bump version to 4.2.1
*   Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 4.1.4-1
-   Upgrade to version 4.1.4
*   Wed Jan 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1.3-4
-   Bump up for depending on readline 7.0
*   Sun Dec 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.1.3-3
-   Provides /bin/awk
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1.3-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 4.1.3-1
-   Updated to version 4.1.3
*   Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.0-2
-   Provide /bin/gawk.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.1.0-1
-   Initial build. First version
