Summary:        GD is an open source code library for the dynamic creation of images by programmers.
Name:           libgd
Version:        2.3.0
Release:        6%{?dist}
License:        MIT
URL:            https://libgd.github.io/
Group:          System/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/libgd/libgd/releases/download/gd-%{version}/%{name}-%{version}.tar.gz
%define sha512  libgd=7e7743bb95bd7fe259515aad9e10afd7c78c52e08fce0fa6ed5b42d4d03230c5c2ab499b02b5a141736fe0865983a852c3896bff0cbbc4fe3edace7edb5d7a67

Patch0:         libgd-CVE-2021-38115.patch
Patch1:         libgd-CVE-2021-40145.patch

BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libwebp-devel
BuildRequires:  libtiff-devel
BuildRequires:  libltdl-devel

Requires:       libpng
Requires:       libwebp
Requires:       libtiff
Requires:       libjpeg-turbo
Provides:       pkgconfig(libgd)

%description
GD is an open source code library for the dynamic creation of images by programmers.

GD is written in C, and "wrappers" are available for Perl, PHP and other languages. GD can read and write many different image formats. GD is commonly used to generate charts, graphics, thumbnails, and most anything else, on the fly.
%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
%description    devel
Header & Development files

%prep
# Using autosetup is not feasible
%setup -c -n %{name}
cd %{name}-gd-%{version}
%patch0 -p1

%build
cd %{name}-gd-%{version}
# To use the system installed automake latest version instead of given version in source
./bootstrap.sh
%configure --with-webp --with-tiff --with-jpeg --with-png --disable-werror --disable-static
make %{?_smp_mflags}
%install
cd %{name}-gd-%{version}
%make_install

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libgd.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libgd.so
%{_libdir}/pkgconfig/*

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.3.0-6
- Remove .la files
* Mon Jun 20 2022 Shivani Agarwal <shivania2@vmware.com>  2.3.0-5
- Version bump up to use libtiff 4.4.0
* Wed Mar 23 2022 HarinadhD <hdommaraju@vmware.com> 2.3.0-4
- Version bumpup to build with libtiff 4.3.0
* Mon Sep 13 2021 Nitesh Kumar <kunitesh@vmware.com> 2.3.0-3
- Fix for CVE-2021-40145.
* Thu Aug 26 2021 Nitesh Kumar <kunitesh@vmware.com> 2.3.0-2
- Fix for CVE-2021-38115.
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
- Automatic Version Bump
* Thu Mar 05 2020 Ankit Jain <ankitja@vmware.com>  2.2.5-4
- Fix for CVE-2019-6977, CVE-2018-14553
* Wed Jan 30 2019 Ankit Jain <ankitja@vmware.com>  2.2.5-3
- Fix for CVE-2019-6978
* Fri Nov 02 2018 Ankit Jain <ankitja@vmware.com>  2.2.5-2
- Fix for CVE-2018-1000222
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.5-1
- Updated to version 2.2.5 to address CVE-2017-6362
* Tue Jan 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.2.4-1
- Updated to version 2.2.4.
* Wed Jan 18 2017 Kumar Kaushik <kaushikk@vmware.com>  2.2.3-3
- Fix for CVE-2016-8670
* Fri Oct 07 2016 Anish Swaminathan <anishs@vmware.com>  2.2.3-2
- Fix for CVE-2016-7568
* Thu Jul 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.3-1
- Initial version
