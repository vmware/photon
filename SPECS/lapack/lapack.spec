Summary:        linear algebra package
Name:           lapack
Version:        3.9.0
Release:        2%{?dist}
URL:            http://www.netlib.org/lapack
License:        BSD
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.netlib.org/%{name}/%{name}-%{version}.tar.gz
%define sha512 %{name}=424956ad941a60a4b71e0d451ad48db12a692f8a71a90f3ca7f71d6ecc1922f392746ea84df1c47a46577ed2db32e9e47ec44ad248207c5ac7da179becb712ef

Patch0: CVE-2021-4048.patch

BuildRequires:  cmake
BuildRequires:  gfortran

%description
LAPACK is written in Fortran 90 and provides routines for solving systems of simultaneous linear equations, least-squares solutions of linear systems of equations, eigenvalue problems, and singular value problems. The associated matrix factorizations (LU, Cholesky, QR, SVD, Schur, generalized Schur) are also provided, as are related computations such as reordering of the Schur factorizations and estimating condition numbers. Dense and banded matrices are handled, but not general sparse matrices. In all areas, similar functionality is provided for real and complex matrices, in both single and double precision.

%package        devel
Summary:        Development files for lapack
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The lapack-devel package contains libraries and header files for
developing applications that use lapack.

%prep
%autosetup -p1

%build
%cmake \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_BUILD_TYPE=Debug \
      -DBUILD_SHARED_LIBS=ON \
      -DLAPACKE=ON

%{cmake_build}

%install
%{cmake_install}
mkdir %{buildroot}%{_includedir}/lapacke
mv %{buildroot}%{_includedir}/*.h %{buildroot}/%{_includedir}/lapacke/.

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libblas.so.*
%{_libdir}/liblapack.so.*
%{_libdir}/liblapacke.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libblas.so
%{_libdir}/liblapack.so
%{_libdir}/liblapacke.so
%{_includedir}/*
%{_libdir}/pkgconfig

%exclude %{_libdir}/cmake/*

%changelog
* Wed Dec 15 2021 Nitesh Kumar <kunitesh@vmware.com> 3.9.0-2
- Fix for CVE-2021-4048.
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.9.0-1
- Automatic Version Bump
* Thu Sep 20 2018 Ankit Jain <ankitja@vmware.com> 3.8.0-1
- Updated to version 3.8.0
* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.0-1
- Initial packaging for Photon
