Summary:        fork of the original IJG libjpeg which uses SIMD.
Name:           libjpeg-turbo
Version:        2.0.0
Release:        1%{?dist}
License:        IJG
URL:            http://sourceforge.net/projects/libjpeg-turbo
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://downloads.sourceforge.net/libjpeg-turbo/%{name}-%{version}.tar.gz
%define sha1    libjpeg-turbo=6d74b609294b6bae5a7cde035f7d6b80d60ebb77
BuildRequires:  nasm
BuildRequires:  cmake

%description
libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline JPEG compression and decompression. libjpeg is a library that implements JPEG image encoding, decoding and transcoding.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications 

%prep
%setup -q

%build
mkdir build
cd build
%{cmake} -DCMAKE_SKIP_RPATH:BOOL=YES \
         -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
         -DENABLE_STATIC:BOOL=NO ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Sun Sep 20 2018 Bo Gan <ganb@vmware.com> 2.0.0-1
-   Update to 2.0.0
-   cmake build system
*   Mon Dec 11 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.2-2
-   Fix CVE-2017-15232
*   Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.2-1
-   Updated to version 1.5.2
*   Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.1-1
-   Updated to version 1.5.1
*   Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
-   Initial version

