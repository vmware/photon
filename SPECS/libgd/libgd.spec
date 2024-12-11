Summary:        GD is an open source code library for the dynamic creation of images by programmers.
Name:           libgd
Version:        2.3.3
Release:        8%{?dist}
URL:            https://libgd.github.io
Group:          System/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/libgd/libgd/releases/download/gd-%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=aa49d4381d604a4360d556419d603df2ffd689a6dcc10f8e5e1d158ddaa3ab89912f6077ca77da4e370055074007971cf6d356ec9bf26dcf39bcff3208bc7e6c

Source1: license.txt
%include %{SOURCE1}

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
GD is written in C, and "wrappers" are available for Perl, PHP and other languages.
GD can read and write many different image formats.
GD is commonly used to generate charts, graphics, thumbnails, and most anything else, on the fly.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libpng-devel

%description    devel
Header & Development files

%prep
%autosetup -n %{name}-%{version} -p1

%build
# To use the system installed automake latest version instead of given version in source
sh ./bootstrap.sh
%configure --with-webp --with-tiff --with-jpeg --with-png --disable-werror --disable-static
%make_build

%install
%make_install

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check
%endif

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
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.3.3-8
- Release bump for SRP compliance
* Wed Jul 17 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.3.3-7
- Add libpng-devel to devel package requires
* Wed Sep 20 2023 Kuntal Nayak <nkuntal@vmware.com> 2.3.3-6
- Bump version as a part of libwebp upgrade
* Fri Jul 28 2023 Kuntal Nayak <nkuntal@vmware.com> 2.3.3-5
- Bump version as a part of libwebp upgrade
* Tue Jul 04 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.3.3-4
- Bump version as a part of libtiff upgrade
* Fri May 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.3.3-3
- Bump version as a part of libtiff upgrade
* Tue Dec 13 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 2.3.3-2
- Bump release as a part of libpng upgrade
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.3.3-1
- Remove .la files
- Upgrade to v2.3.3
* Mon Jun 20 2022 Shivani Agarwal <shivania2@vmware.com>  2.3.2-4
- Version bump up to use libtiff 4.4.0
* Fri Sep 24 2021 Nitesh Kumar <kunitesh@vmware.com> 2.3.2-3
- Patched for CVE-2021-40812.
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 2.3.2-2
- Patched for CVE-2021-38115 and CVE-2021-40145.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.3.2-1
- Automatic Version Bump
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
