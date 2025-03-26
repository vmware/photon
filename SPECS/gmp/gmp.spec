Summary:         Math libraries
Name:            gmp
Version:         6.2.1
Release:         4%{?dist}
URL:             http://www.gnu.org/software/gmp
Group:           Applications/System
Vendor:          VMware, Inc.
Distribution:    Photon

Source0: http://ftp.gnu.org/gnu/gmp/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Patch0: mpz-inp_raw-avoid-bit-size-overflows.patch

%description
The GMP package contains math libraries. These have useful functions
for arbitrary precision arithmetic.

%package    devel
Summary:    Header and development files for gmp
Requires:   %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications
for handling compiled objects.

%prep
%autosetup -p1

%build

%ifarch x86_64
# Do not detect host's CPU. Generate generic library (-mtune=k8)
cp -v configfsf.guess config.guess
cp -v configfsf.sub config.sub
%endif

%configure \
    --disable-silent-rules \
    --disable-static \
    --disable-assembly

make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -v doc/{isa_abi_headache,configuration} doc/*.html %{buildroot}%{_defaultdocdir}/%{name}-%{version}
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libgmp.so.*

%files devel
%{_includedir}/gmp.h
%{_libdir}/libgmp.so
%{_libdir}/pkgconfig/*.pc
%{_docdir}/%{name}-%{version}/tasks.html
%{_docdir}/%{name}-%{version}/projects.html
%{_docdir}/%{name}-%{version}/configuration
%{_docdir}/%{name}-%{version}/isa_abi_headache

%changelog
*   Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.2.1-4
-   Release bump for SRP compliance
*   Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 6.2.1-3
-   Bump version to generate SRP provenance file
*   Mon Nov 13 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 6.2.1-2
-   Add patch to fix CVE-2021-43618
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 6.2.1-1
-   Automatic Version Bump
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 6.2.0-1
-   Automatic Version Bump
*   Wed Sep 04 2019 Alexey Makhalov <amakhalov@vmware.com> 6.1.2-3
-   Use -mtune -march options for generic CPU (x86_64)
*   Tue Apr 18 2017 Alexey Makhalov <amakhalov@vmware.com> 6.1.2-2
-   Disable cxx (do not build libgmpxx). Disable static.
*   Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 6.1.2-1
-   Update to 6.1.2
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.0a-3
-   GA - Bump release of all rpms
*   Thu Apr 14 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 6.0.0a-2
-   Disable assembly and use generic C code
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 6.0.0a-1
-   Updated to version 6.0.0
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.1.3-1
-   Initial build. First version
