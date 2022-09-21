%define debug_package %{nil}

Summary:        aws sdk for c++
Group:          Development/Libraries
Name:           aws-sdk-cpp
Version:        1.4.33
Release:        5%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
Url:            https://github.com/aws/aws-sdk-cpp

Source0: https://github.com/aws/aws-sdk-cpp/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=ebe8e402107b7b70a9b397c94ad981ff02d97e10e6fd8337f19b732185ecbb79e132eecd513300ce733a765fd780dd765c1d2b34479e5e1d891fa771722bad81

Patch0:         aws-sdk-cpp-Build-foxes-for-GCC9.patch

Requires:       openssl-devel
Requires:       curl-devel
Requires:       zlib-devel
Requires:       aws-sdk-core = %{version}-%{release}
Requires:       aws-sdk-kinesis = %{version}-%{release}
Requires:       aws-sdk-s3 = %{version}-%{release}

BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
The AWS SDK for C++ provides a modern C++ (version C++ 11 or later) interface for Amazon Web Services (AWS).

%package -n     aws-sdk-core
Summary:        aws sdk core
Group:          Development/Libraries
Requires:       aws-core-libs = %{version}-%{release}

%description -n aws-sdk-core
aws sdk cpp core

%package -n     aws-core-libs
Summary:        aws core libs
Group:          Development/Libraries
Requires:       openssl-devel
Requires:       curl-devel
Requires:       zlib-devel

%description -n aws-core-libs
aws core libs

%package -n     aws-sdk-kinesis
Summary:        aws sdk kinesis
Group:          Development/Libraries
Requires:       aws-sdk-core = %{version}-%{release}
Requires:       aws-kinesis-libs = %{version}-%{release}

%description -n aws-sdk-kinesis
aws sdk cpp for kinesis

%package -n     aws-kinesis-libs
Summary:        aws kinesis libs
Group:          Development/Libraries
Requires:       aws-core-libs = %{version}-%{release}

%description -n aws-kinesis-libs
aws kinesis libs

%package -n     aws-sdk-s3
Summary:        aws sdk s3
Group:          Development/Libraries
Requires:       aws-sdk-core = %{version}-%{release}
Requires:       aws-s3-libs = %{version}-%{release}

%description -n aws-sdk-s3
aws sdk cpp for s3

%package -n     aws-s3-libs
Summary:        aws s3 libs
Group:          Development/Libraries
Requires:       aws-core-libs = %{version}-%{release}

%description -n aws-s3-libs
aws s3 libs

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

cd %{__cmake_builddir}
for component in "core" "kinesis" "s3"; do
  pushd aws-cpp-sdk-$component
  make %{?_smp_mflags}
  popd
done

%install
cd %{__cmake_builddir}
for component in "core" "kinesis" "s3"; do
  pushd aws-cpp-sdk-$component
  make DESTDIR=%{buildroot} install %{?_smp_mflags}
  popd
done

rm -rf %{buildroot}%{_libdir}/cmake

%clean
rm -rf %{buildroot}/*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,0755)
%exclude %{_includedir}/aws/core
%exclude %{_includedir}/aws/kinesis
%exclude %{_includedir}/aws/s3
%exclude %{_libdir}/pkgconfig/aws-cpp-sdk-core.pc
%exclude %{_libdir}/pkgconfig/aws-cpp-sdk-kinesis.pc
%exclude %{_libdir}/pkgconfig/aws-cpp-sdk-s3.pc
%exclude %{_libdir}/libaws-cpp-sdk-core.so
%exclude %{_libdir}/libaws-cpp-sdk-kinesis.so
%exclude %{_libdir}/libaws-cpp-sdk-s3.so

%files -n aws-sdk-core
%defattr(-,root,root,0755)
%{_includedir}/aws/core/*
%{_libdir}/pkgconfig/aws-cpp-sdk-core.pc

%files -n aws-core-libs
%defattr(-,root,root,0755)
%{_libdir}/libaws-cpp-sdk-core.so

%files -n aws-sdk-kinesis
%defattr(-,root,root,0755)
%{_includedir}/aws/kinesis/*
%{_libdir}/pkgconfig/aws-cpp-sdk-kinesis.pc

%files -n aws-kinesis-libs
%defattr(-,root,root,0755)
%{_libdir}/libaws-cpp-sdk-kinesis.so

%files -n aws-sdk-s3
%defattr(-,root,root,0755)
%{_includedir}/aws/s3/*
%{_libdir}/pkgconfig/aws-cpp-sdk-s3.pc

%files -n aws-s3-libs
%defattr(-,root,root,0755)
%{_libdir}/libaws-cpp-sdk-s3.so

%changelog
* Thu Sep 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.33-5
- Use cmake macros
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.4.33-4
- Bump up release for openssl
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.4.33-3
- openssl 1.1.1
* Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 1.4.33-2
- Fix compilation issue with gcc-8.4.0
* Thu Aug 30 2018 Anish Swaminathan <anishs@vmware.com> 1.4.33-1
- Initial build.  First version
