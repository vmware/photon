Summary:        TIFF libraries and associated utilities.
Name:           libtiff
Version:        4.5.1
Release:        6%{?dist}
License:        libtiff
URL:            http://www.libtiff.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://download.osgeo.org/%{name}/tiff-%{version}.tar.xz
%define sha512 tiff=fc6af93d36598527480c517ddc4f19fe72e9f07ef4997e5731604253c8db0b9bae816ba7a56985bf22fbbb48db1fab5ed4c2b32a5145bc9477ef24b221a61179

Patch0:         CVE-2023-40745.patch
Patch1:         CVE-2023-41175.patch
Patch2:         CVE-2023-6277.patch
Patch3:         CVE-2023-52355.patch
Patch4:         CVE-2023-52356.patch
Patch5:         CVE-2024-7006.patch

BuildRequires:  libjpeg-turbo-devel

Requires:       libjpeg-turbo

%description
The LibTIFF package contains the TIFF libraries and associated utilities. The libraries are used by many programs for reading and writing TIFF files and the utilities are used for general work with TIFF files.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libjpeg-turbo-devel
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -n tiff-%{version} -p1

%build
%configure \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/doc/*
%{_mandir}/man*/*

%changelog
* Mon Sep 02 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.5.1-6
- Fix build regression due to random download failures at build time
* Thu Aug 22 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 4.5.1-5
- Fix CVE-2024-7006
* Mon Jan 29 2024  Anmol Jain <anmolja@vmware.com> 4.5.1-4
- Fix for CVE-2023-52355 & CVE-2023-52356
* Wed Dec 13 2023 Anmol Jain <anmolja@vmware.com> 4.5.1-3
- Fix for CVE-2023-6277
* Wed Oct 18 2023 Anmol Jain <anmolja@vmware.com> 4.5.1-2
- Fix for CVE-2023-40745, CVE-2023-41175
* Fri Jul 07 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.5.1-1
- Update to v4.5.1
* Wed Jul 05 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.5.0-5
- Fix for CVE-2023-2731/CVE-2023-3316
* Mon Jul 03 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.5.0-4
- Fix for CVE-2023-25433/2023-26966
* Mon Jun 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.5.0-3
- Fix for CVE-2023-0798/2023-0804/2023-26965
* Mon Feb 06 2023 Anmol Jain <anmolja@vmware.com> 4.5.0-2
- Fix for CVE-2022-48281
* Fri Jan 06 2023 Anmol Jain <anmolja@vmware.com> 4.5.0-1
- Version Update
* Sun Nov 20 2022 Anmol Jain <anmolja@vmware.com> 4.4.0-7
- Fix CVE-2022-3970
* Tue Oct 25 2022 Anmol Jain <anmolja@vmware.com> 4.4.0-6
- Fix CVE-2022-3570
* Thu Sep 08 2022 Anmol Jain <anmolja@vmware.com> 4.4.0-5
- Fix CVE-2022-2953
* Tue Aug 16 2022 Anmol Jain <anmolja@vmware.com> 4.4.0-4
- Fix CVE-2022-34526
* Mon Jul 11 2022 Shivani Agarwal <shivania2@vmware.com> 4.4.0-3
- Fix CVE-2022-2056
* Wed Jun 22 2022 Shivani Agarwal <shivania2@vmware.com> 4.4.0-2
- Removed obsolete patch CVE-2018-12900.patch
* Mon May 30 2022 Shivani Agarwal <shivania2@vmware.com> 4.4.0-1
- Fix CVE-2022-1622, CVE-2022-22844, CVE-2022-0865, CVE-2022-0924, CVE-2022-0908, CVE-2022-0909, CVE-2022-0907
* Mon Mar 21 2022 Harinadh D <hdommaraju@vmware.com> 4.3.0-1
- Fix CVE-2022-0891,CVE-2022-0562
* Fri Mar 11 2022 Harinadh D <hdommaraju@vmware.com> 4.1.0-4
- Fix CVE-2022-0561
* Mon Sep 20 2021 Harinadh D <hdommaraju@vmware.com> 4.1.0-3
- Fix CVE-2020-35521
* Mon Mar 22 2021 Harinadh D <hdommaraju@vmware.com> 4.1.0-2
- Fix CVE-2020-35523 , CVE-2020-35524
* Fri Apr 03 2020 Sujay G <gsujay@vmware.com> 4.1.0-1
- Bump version to 4.1.0
* Mon Nov 18 2019 Anisha Kumari <kanisha@vmware.com> 4.0.10-5
- Fix for CVE-2019-17546
* Mon Jun 03 2019 Ashwin H <ashwinh@vmware.com> 4.0.10-4
- Fix for CVE-2019-7663
* Tue Feb 05 2019 Keerthana K <keerthanak@vmware.com> 4.0.10-3
- Fix for CVE-2019-6128.
* Mon Jan 28 2019 Keerthana K <keerthanak@vmware.com> 4.0.10-2
- Fix for CVE-2018-12900
* Mon Dec 10 2018 Ashwin H <ashwinh@vmware.com> 4.0.10-1
- Update to 4.0.10
* Sun Dec 02 2018 Ashwin H <ashwinh@vmware.com> 4.0.9-5
- Fix CVE-2018-17100, CVE-2018-17101
* Mon May 14 2018 Xiaolin Li <xiaolinl@vmware.com> 4.0.9-4
- Fix CVE-2018-7456, CVE-2018-8905, CVE-2018-5784, CVE-2017-11613
* Wed Feb 14 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-3
- Patch for CVE-2017-17095
* Wed Jan 31 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-2
- Repatched CVE-2017-9935
* Wed Jan 17 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-1
- Updated to version 4.0.9 to fix CVE-2017-11613, CVE-2017-9937,
- CVE-2017-17973. Added a patch for CVE-2017-18013
* Mon Dec 11 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-7
- Added patch for CVE-2017-9935
* Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-6
- Added patches for CVE-2017-13726, CVE-2017-13727
* Mon Nov 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.0.8-5
- Patch : CVE-2017-12944
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.8-4
- Use standard configure macros
* Wed Aug 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.8-3
- Added patch for CVE-2017-9936, CVE-2017-11335
* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 4.0.8-2
- Applied patch for CVE-2017-10688
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-1
- Updated to version 4.0.8.
* Tue May 16 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.7-4
- Added patch for CVE-2016-10266, CVE-2016-10268, CVE-2016-10269, CVE-2016-10267 and libtiff-heap-buffer-overflow patch
* Mon Apr 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.0.7-3
- Patch : CVE-2016-10092, CVE-2016-10093, CVE-2016-10094
* Thu Jan 19 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.0.7-2
- Patch : CVE-2017-5225
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.0.7-1
- Update to 4.0.7. It fixes CVE-2016-953[3456789] and CVE-2016-9540
- Remove obsolete patches
* Wed Oct 12 2016 Dheeraj Shetty <dheerajs@vmware.com> 4.0.6-3
- Fixed security issues : CVE-2016-3945, CVE-2016-3990, CVE-2016-3991
* Thu Sep 22 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.6-2
- Fixed security issues : CVE-2015-8668, CVE-2015-7554, CVE-2015-8683+CVE-2015-8665,CVE-2016-3186
- CVE-2015-1547
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 4.0.6-1
- Initial version
