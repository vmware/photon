Summary:        Build tool
Name:           pkg-config
Version:        0.29.2
Release:        5%{?dist}
URL:            http://www.freedesktop.org/wiki/Software/pkg-config
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://pkgconfig.freedesktop.org/releases/%{name}-%{version}.tar.gz
%define sha512 %{name}=4861ec6428fead416f5cbbbb0bbad10b9152967e481d4b0ff2eb396a9f297f552984c9bb72f6864a37dcd8fca1d9ccceda3ef18d8f121938dbe4fdf2b870fe75

Source1: license.txt
%include %{SOURCE1}

Patch0:         pkg-config-glib-CVE-2018-16428.patch
Patch1:         pkg-config-glib-CVE-2018-16429.patch

%description
Contains a tool for passing the include path and/or library paths
to build tools during the configure and make file execution.

%prep
# Using autosetup is not feasible
%setup -q
cd glib  # patches need to apply to internal glib
%patch0 -p1
%patch1 -p1
cd ..

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
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/pkg-config
%{_datadir}/aclocal/pkg.m4
%{_docdir}/pkg-config-*/pkg-config-guide.html
%{_mandir}/man1/pkg-config.1.gz
%changelog
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.29.2-5
- Release bump for SRP compliance
* Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.29.2-4
- Bump version to generate SRP provenance file
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
