Name:           libbsd
Version:        0.12.2
Release:        1%{?dist}
Summary:        Library providing BSD-compatible functions for portability
URL:            https://libbsd.freedesktop.org
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.xz

# Taken from:
# https://src.fedoraproject.org/rpms/libbsd/blob/f41/f/libbsd-cdefs.h
Source1: %{name}-cdefs.h

Source2: license.txt
%include %{SOURCE2}

BuildRequires: libmd-devel

Requires: libmd

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package devel
Summary:        Development files for libbsd
Requires:       %{name} = %{version}-%{release}
Requires:       libmd-devel

%description devel
Development files for the libbsd library.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_mandir}

# avoid file conflicts in multilib installations of -devel subpackage
mv -f %{buildroot}%{_includedir}/bsd/sys/cdefs{,-%{__isa_bits}}.h
install -p -m 0644 %{SOURCE1} %{buildroot}%{_includedir}/bsd/sys/cdefs.h

find %{buildroot}%{_libdir} -name "*.a" -delete
rm -f %{buildroot}%{_libdir}/pkgconfig/libbsd-ctor.pc

%if 0%{?with_check}
%check
%make_build check
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/bsd
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-overlay.pc

%changelog
* Tue Sep 10 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.12.2-1
- Initial version. Needed by libretls.
