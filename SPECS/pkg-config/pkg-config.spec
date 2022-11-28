Summary:	Build tool
Name:		pkg-config
Version:	0.29.2
Release:	5%{?dist}
License:	GPLv2+
URL:		http://www.freedesktop.org/wiki/Software/pkg-config
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://pkgconfig.freedesktop.org/releases/%{name}-%{version}.tar.gz
%define sha512 pkg-config=4861ec6428fead416f5cbbbb0bbad10b9152967e481d4b0ff2eb396a9f297f552984c9bb72f6864a37dcd8fca1d9ccceda3ef18d8f121938dbe4fdf2b870fe75
Patch0:         pkg-config-glib-CVE-2018-16428.patch
Patch1:         pkg-config-glib-CVE-2018-16429.patch
Patch2:         pkg-config-glib-CVE-2020-35457.patch
Patch3:         pkg-config-glib-CVE-2021-27218.patch
Patch4:         pkg-config-glib-CVE-2021-3800.patch

%description
Contains a tool for passing the include path and/or library paths
to build tools during the configure and make file execution.

%prep
%autosetup -p1

%build
if [ %{_host} != %{_build} ]; then
# configure unable to run tests for cross compilation
# preset values
    export glib_cv_stack_grows=no
    export ac_cv_func_posix_getpwuid_r=yes
    export ac_cv_func_posix_getgrgid_r=yes
    export glib_cv_uscore=yes
fi
%configure \
    --target=%{_host} \
    --with-internal-glib \
    --disable-host-tool \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-silent-rules
%make_build

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/pkg-config
%{_datadir}/aclocal/pkg.m4
%{_docdir}/pkg-config-*/pkg-config-guide.html
%{_mandir}/man1/pkg-config.1.gz

%changelog
* Mon Nov 28 2022 Harinadh D <hdommaraju@vmware.com> 0.29.2-5
- fix CVE-2021-3800
* Tue Dec 07 2021 Mukul Sikka <msikka@vmware.com> 0.29.2-4
- Fix internal glib for CVE-2020-35457 and CVE-2021-27218
* Wed Jul 03 2019 Alexey Makhalov <amakhalov@vmware.com> 0.29.2-3
- Cross compilation support
* Fri Jan 18 2019 Ajay Kaher <akaher@vmware.com> 0.29.2-2
- Fix internal glib for CVE-2018-16428 and CVE-2018-16429
* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 0.29.2-1
- upgrade for 2.0
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 0.28-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.28-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 0.28-1
- Initial build. First version
