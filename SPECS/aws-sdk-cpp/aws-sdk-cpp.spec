%define debug_package %{nil}
Summary:        aws sdk for c++
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
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
The AWS SDK for C++ provides a modern C++ (version C++ 11 or later) interface for Amazon Web Services (AWS).

%prep
%setup

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ..
make %{?_smp_mflags}


%install
cd build
make DESTDIR=%{buildroot} install

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
    %{_libdir}/*
    %{_includedir}/*

%changelog
*   Wed Apr 11 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.33-1
-   Initial build.  First version
