Name:           libbsd
Version:        0.12.2
Release:        1%{?dist}
Summary:        Library providing BSD-compatible functions for portability
URL:            https://libbsd.freedesktop.org
# Breakdown in COPYING file of libbsd release tarball, see also:
# - https://gitlab.com/fedora/legal/fedora-license-data/-/issues/71
# - https://gitlab.com/fedora/legal/fedora-license-data/-/issues/73
License:        Beerware AND BSD-2-Clause AND BSD-3-Clause AND ISC AND libutil-David-Nugent AND MIT AND LicenseRef-Fedora-Public-Domain
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.xz
%define sha512 %{name}=ce43e4f0486d5f00d4a8119ee863eaaa2f968cae4aa3d622976bb31ad601dfc565afacef7ebade5eba33fff1c329b5296c6387c008d1e1805d878431038f8b21

# Taken from:
# https://src.fedoraproject.org/rpms/libbsd/blob/f41/f/libbsd-cdefs.h
Source3: libbsd-cdefs.h

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
install -p -m 0644 %{SOURCE3} %{buildroot}%{_includedir}/bsd/sys/cdefs.h

find %{buildroot}%{_libdir} -name "*.a" -delete
rm -f %{buildroot}%{_libdir}/pkgconfig/libbsd-ctor.pc

%check
%make_build check

%ldconfig_scriptlets

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
