Summary:        Crypto Libraries
Name:           libgcrypt
Version:        1.10.1
Release:        3%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            http://www.gnu.org/software/libgcrypt
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
%define sha512  %{name}=e5ca7966624fff16c3013795836a2c4377f0193dbb4ac5ad2b79654b1fa8992e17d83816569a402212dc8367a7980d4141f5d6ac282bae6b9f02186365b61f13

BuildRequires:  libgpg-error-devel

Requires:       libgpg-error

%description
The libgcrypt package contains a general purpose crypto library based on the code used in GnuPG.
The library provides a high level interface to cryptographic building blocks using an extendable and flexible API.

%package        devel
Summary:        Development libraries and header files for libgcrypt
Requires:       %{name} = %{version}-%{release}
Requires:       libgpg-error-devel

%description    devel
The package contains libraries and header files for developing applications that use libgcrypt.

%prep
%autosetup -p1

%build
if [ %{_host} != %{_build} ]; then
%configure \
    --with-sysroot=/target-%{_arch} \
    ac_cv_sys_symbol_underscore=no
else
%configure
fi

%make_build

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_infodir} \
       %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_datadir}/aclocal/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgcrypt.pc

%changelog
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.10.1-3
- Bump release as a part of libgpg-error upgrade to 1.46
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.1-2
- Remove .la files
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.10.1-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.9.3-1
- Automatic Version Bump
* Tue Jul 28 2020 Ankit Jain <ankitja@vmware.com> 1.8.6-2
- Release Bump up to fix libgpg-error build issue
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.8.6-1
- Automatic Version Bump
* Thu Oct 17 2019 Ankit Jain <ankitja@vmware.com> 1.8.5-1
- Updated to version 1.8.5
* Tue Nov 06 2018 Sriram Nambakam <snambakam@vmware.com> 1.8.3-2
- Cross compilation support
* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.8.3-1
- Update to 1.8.3
* Tue Oct 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.1-1
- Updated to v1.8.1 to address CVE-2017-0379
* Tue Apr 04 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.6-1
- Udpated to version 1.7.6
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6.5-3
- Required libgpg-error-devel.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.5-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  1.6.5-1
- Upgrade to 1.6.5
* Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.3-1
- Initial build. First version.
