Summary:        Contains a utility for determining file types
Name:           file
Version:        5.43
Release:        3%{?dist}
URL:            http://www.darwinsys.com/file
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Requires:       %{name}-libs = %{version}-%{release}

Conflicts:      toybox < 0.8.2-2

%description
The package contains a utility for determining the type of a
given file or files

%package        libs
Summary:        Library files for file
%description    libs
It contains the libraries to run the application.

%package        devel
Summary:        Header and development files for file
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*man1/*
%{_mandir}/*man4/*

%files  libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datarootdir}/misc/magic.mgc

%files  devel
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/*man3/*
%{_libdir}/pkgconfig/libmagic.pc

%changelog
*   Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.43-3
-   Release bump for SRP compliance
*   Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 5.43-2
-   Bump version to generate SRP provenance file
*   Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 5.43-1
-   Automatic Version Bump
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 5.41-1
-   Automatic Version Bump
*   Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 5.40-1
-   Automatic Version Bump
*   Thu Feb 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.39-2
-   Fix close_on_exec multithreaded decompression issue
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 5.39-1
-   Automatic Version Bump
*   Tue Jul 07 2020 Gerrit Photon <photon-checkins@vmware.com> 5.38-1
-   Automatic Version Bump
*   Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 5.34-3
-   Do not conflict with toybox >= 0.8.2-2
*   Tue Oct 29 2019 Siju Maliakkal <smaliakkal@vmware.com> 5.34-2
-   Apply patch for CVE-2019-18218
*   Thu Sep 20 2018 Sujay G <gsujay@vmware.com> 5.34-1
-   Bump file version to 5.34
*   Fri Dec 15 2017 Divya Thaluru <dthaluru@vmware.com> 5.30-3
-   Added seperate package for libraries
-   Added toybox as conflict package
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 5.30-2
-   Add devel package.
*   Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 5.30-1
-   Updated to version 5.30
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.24-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 5.24-1
-   Updated to version 5.24
*   Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 5.22-1
-   Initial build. First version.
