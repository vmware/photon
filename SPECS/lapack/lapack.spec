Summary:        linear algebra package
Name:           lapack
Version:        3.10.1
Release:        1%{?dist}
URL:            http://www.netlib.org/lapack/
License:        BSD
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.netlib.org/%{name}/%{name}-%{version}.tar.gz
%define         sha512 %{name}=0500bbbb48483208c0a35b74972ff0059c389da6032824a2079637266a99fa980882eedf7f1fc490219ee4ff27812ac8c6afe118e25f40a9c2387e7b997762fb

BuildRequires:  cmake
BuildRequires:  gfortran

%description
LAPACK is written in Fortran 90 and provides routines for solving systems of simultaneous linear equations, least-squares solutions of linear systems of equations, eigenvalue problems, and singular value problems. The associated matrix factorizations (LU, Cholesky, QR, SVD, Schur, generalized Schur) are also provided, as are related computations such as reordering of the Schur factorizations and estimating condition numbers. Dense and banded matrices are handled, but not general sparse matrices. In all areas, similar functionality is provided for real and complex matrices, in both single and double precision.

%package        devel
Summary:        Development files for lapack
Group:          Development/Libraries
Requires:       lapack = %{version}-%{release}

%description    devel
The lapack-devel package contains libraries and header files for
developing applications that use lapack.

%prep
%autosetup

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_BUILD_TYPE=Release        \
      -DBUILD_SHARED_LIBS=ON            \
      -DLAPACKE=ON                      \
      ..

make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd build
make DESTDIR=%{buildroot} install %{?_smp_mflags}
mkdir %{buildroot}/%{_includedir}/lapacke
mv %{buildroot}/%{_includedir}/*.h %{buildroot}/%{_includedir}/lapacke/.

%ldconfig_scriptlets

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
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.10.1-1
- Automatic Version Bump
* Wed Dec 15 2021 Nitesh Kumar <kunitesh@vmware.com> 3.9.1-2
- Fix for CVE-2021-4048.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.9.1-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.9.0-1
- Automatic Version Bump
* Thu Sep 20 2018 Ankit Jain <ankitja@vmware.com> 3.8.0-1
- Updated to version 3.8.0
* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.0-1
- Initial packaging for Photon
