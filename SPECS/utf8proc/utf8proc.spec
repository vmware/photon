Summary:        C library that provide processing for data in the UTF-8 encoding
Name:           utf8proc
Version:        2.5.0
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Libraries
Url:            https://github.com/JuliaStrings/utf8proc
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:  https://github.com/JuliaStrings/utf8proc/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=0c553faf4f3841c17c7aa4cce1e917b1585c430ac3f7f240ab98cbe01b9743f2074532e6f71faf3df030f5af00e483a3faf9716a67e6a4b1bb66a3de48308014

BuildRequires:  cmake

%description
utf8proc is a small, clean C library that provides Unicode normalization, case-folding, and other operations for data in the UTF-8 encoding.

%package        devel
Summary:        Development libraries and headers for utf8proc
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The utf8proc-devel package contains libraries, header files and documentation
for developing applications that use utf8proc.

%prep
%autosetup -p1

%build
%cmake \
      -DCMAKE_BUILD_TYPE=Debug \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc lump.md LICENSE.md NEWS.md README.md
%{_libdir}/libutf8proc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/utf8proc.h
%{_libdir}/libutf8proc.so

%changelog
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.0-1
- Automatic Version Bump
* Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 2.2.0-1
- Initial Version.
