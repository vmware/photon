%define debug_package %{nil}
Summary:        aws sdk for c++
Group:          Development/Libraries
Name:           aws-sdk-cpp
Version:        1.4.33
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
Url:            https://github.com/aws/aws-sdk-cpp
Source0:        aws-sdk-cpp-%{version}.tar.gz
%define sha1    aws-sdk-cpp=5db6bed30cb85c59c7a3a58034f222007e6a9e49
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
%setup

%build
mkdir build
cd build
cmake \
-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
-DCMAKE_BUILD_TYPE=Release ..
for component in "core" "kinesis" "s3"; do
  cd aws-cpp-sdk-$component
  make %{?_smp_mflags}
  cd ..
done


%install
cd build
for component in "core" "kinesis" "s3"; do
  cd aws-cpp-sdk-$component
  make DESTDIR=%{buildroot} install
  cd ..
done
rm -rf %{buildroot}%{_lib64dir}/cmake

%clean
rm -rf %{buildroot}/*

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%files
    %defattr(-,root,root,0755)
    %exclude %{_includedir}/aws/core
    %exclude %{_includedir}/aws/kinesis
    %exclude %{_includedir}/aws/s3
    %exclude %{_lib64dir}/pkgconfig/aws-cpp-sdk-core.pc
    %exclude %{_lib64dir}/pkgconfig/aws-cpp-sdk-kinesis.pc
    %exclude %{_lib64dir}/pkgconfig/aws-cpp-sdk-s3.pc
    %exclude %{_lib64dir}/libaws-cpp-sdk-core.so
    %exclude %{_lib64dir}/libaws-cpp-sdk-kinesis.so
    %exclude %{_lib64dir}/libaws-cpp-sdk-s3.so

%files -n aws-sdk-core
    %defattr(-,root,root,0755)
    %{_includedir}/aws/core/*
    %{_lib64dir}/pkgconfig/aws-cpp-sdk-core.pc

%files -n aws-core-libs
    %defattr(-,root,root,0755)
    %{_lib64dir}/libaws-cpp-sdk-core.so

%files -n aws-sdk-kinesis
    %defattr(-,root,root,0755)
    %{_includedir}/aws/kinesis/*
    %{_lib64dir}/pkgconfig/aws-cpp-sdk-kinesis.pc

%files -n aws-kinesis-libs
    %defattr(-,root,root,0755)
    %{_lib64dir}/libaws-cpp-sdk-kinesis.so

%files -n aws-sdk-s3
    %defattr(-,root,root,0755)
    %{_includedir}/aws/s3/*
    %{_lib64dir}/pkgconfig/aws-cpp-sdk-s3.pc

%files -n aws-s3-libs
    %defattr(-,root,root,0755)
    %{_lib64dir}/libaws-cpp-sdk-s3.so

%changelog
*   Thu Aug 30 2018 Anish Swaminathan <anishs@vmware.com> 1.4.33-1
-   Initial build.  First version
