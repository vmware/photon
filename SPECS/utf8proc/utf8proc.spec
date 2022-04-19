Summary:        C library that provide processing for data in the UTF-8 encoding
Name:           utf8proc
Version:        2.7.0
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Libraries
Url:            https://github.com/JuliaStrings/utf8proc
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=29f7883de13302d609e8755872ed43174e70076e9681b4ac3f9b03e50295c45d9972c193bc81f94ad7e11e2d33a46cad5a30a80873173e6e1ae242101ebb3bed
Vendor:         VMware, Inc.
Distribution:   Photon
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
%autosetup

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_BUILD_TYPE=Release        \
      -DBUILD_SHARED_LIBS=ON            \
      ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
make check %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc lump.md LICENSE.md NEWS.md README.md
%{_lib64dir}/libutf8proc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/utf8proc.h
%{_lib64dir}/libutf8proc.so
%{_lib64dir}/pkgconfig/libutf8proc.pc

%changelog
*       Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-1
-       Automatic Version Bump
*       Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.6.1-1
-       Automatic Version Bump
*       Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.0-1
-       Automatic Version Bump
*       Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 2.2.0-1
-       Initial Version.
