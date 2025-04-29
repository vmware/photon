Summary:        Library that provides message digest functions from BSD systems
Name:           libmd
Version:        1.1.0
Release:        1%{?dist}
URL:            https://www.hadrons.org/software/libmd/
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://libbsd.freedesktop.org/releases/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

%description
The libmd library provides a few message digest ("hash") functions, as
found on various BSD systems, either on their libc or on a library with
the same name, and with a compatible API.

%package devel
Summary:        Development files for the message digest library
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config

%description devel
The libmd-devel package includes header files and libraries necessary
for developing programs which use the message digest library.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install

rm -rf %{buildroot}%{_mandir}

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
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*.h

%changelog
* Wed Sep 18 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.0-1
- Initial version, needed by libbsd.
