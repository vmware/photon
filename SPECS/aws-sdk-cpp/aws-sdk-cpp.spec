%define debug_package %{nil}

Summary:        aws sdk for c++
Group:          Development/Libraries
Name:           aws-sdk-cpp
Version:        1.11.117
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
URL:            https://github.com/aws/aws-sdk-cpp

# Steps to create source tarball
# Download the tag from github, extract it
# Then run `prefetch_crt_dependency.sh` script to get all dependencies
# Example:
# wget https://github.com/aws/aws-sdk-cpp/archive/refs/tags/1.10.20.tar.gz
# tar xf 1.10.20.tar.gz
# cd aws-sdk-cpp-1.10.20 && ./prefetch_crt_dependency.sh && cd -
# tar -I 'gzip -9' -cpf aws-sdk-cpp-1.10.20.tar.gz aws-sdk-cpp-1.10.20
Source0: https://github.com/aws/aws-sdk-cpp/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=c398d2e5176d7369ea571aaa58ac240876929d5f97226de17282baeaadc0d7e20a3f2e8d4d348fbd3eaa365e09ad55631c0f6bb0d52b8a38c3ac935def5165c6

Requires: openssl-devel
Requires: curl-devel
Requires: zlib-devel
Requires: aws-sdk-core = %{version}-%{release}
Requires: aws-sdk-kinesis = %{version}-%{release}
Requires: aws-sdk-s3 = %{version}-%{release}

BuildRequires: cmake
BuildRequires: curl-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

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
# TODO: try to remove -Wno-stringop-truncation flag in future version upgrades
export CXXFLAGS="%{optflags} -Wno-stringop-truncation"
%{cmake} \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

cd %{__cmake_builddir}

pushd ./src/aws-cpp-sdk-core
%make_build
popd

for component in "kinesis" "s3"; do
  pushd ./generated/src/aws-cpp-sdk-${component}
  %make_build
  popd
done

%install
cd %{__cmake_builddir}

pushd ./src/aws-cpp-sdk-core
%make_install %{?_smp_mflags}
popd

for component in  "kinesis" "s3"; do
  pushd ./generated/src/aws-cpp-sdk-${component}
  %make_install %{?_smp_mflags}
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

%files -n aws-sdk-core
%defattr(-,root,root,0755)
%{_includedir}/aws/core/*
%{_includedir}/smithy/*
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
* Wed Jul 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.11.117-1
- Upgrade to v1.11.117
* Fri Apr 14 2023 Harinadh D <hdommaraju@vmware.com> 1.11.58-1
- version upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10.30-2
- Bump version as a part of zlib upgrade
* Thu Dec 15 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.30-1
- Upgrade to v1.10.30
* Thu Dec 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.20-1
- Upgrade to v1.10.20
* Mon Sep 19 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.4.33-6
- Fix build with latest toolchain
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.33-5
- Use cmake macros for build and install
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.4.33-4
- Bump up release for openssl
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.4.33-3
- openssl 1.1.1
* Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 1.4.33-2
- Fix compilation issue with gcc-8.4.0
* Thu Aug 30 2018 Anish Swaminathan <anishs@vmware.com> 1.4.33-1
- Initial build.  First version
