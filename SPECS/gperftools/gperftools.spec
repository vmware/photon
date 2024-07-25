Summary:        A fast malloc tool for threads
Name:           gperftools
Version:        2.10
Release:        2%{?dist}
License:        BSD
URL:            https://github.com/gperftools/gperftools
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/gperftools/gperftools/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=81f3b913e76641c6e51cdfe741fd0028bf9237e3e0f3937ea692ff420c8d006ee01be220417833e55809514fb88eeb0b695fa0a2cac614e60234b8c019a6e92a

%description
gperftools is a collection of a high-performance multi-threaded malloc() implementation,
plus some pretty nifty performance analysis tools.

%package devel
Summary:        gperftools devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description devel
This contains development tools and libraries for gperftools.

%package docs
Summary:        gperftools docs
Group:          Development/Tools
%description docs
The contains gperftools package doc files.

%prep
%autosetup -p1

%build
%configure \
    --docdir=%{_docdir}/%{name}-%{version}

%make_build

%install
%make_install %{?_smp_mflags}

%check
TCMALLOC_SAMPLE_PARAMETER=128 \
    %make_build check

%files
%defattr(-,root,root)
%{_bindir}/pprof
%{_bindir}/pprof-symbolize
%{_libdir}/libprofiler*.so.*
%{_libdir}/libtcmalloc*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/google/*
%{_includedir}/gperftools/*
%{_libdir}/libprofiler*.a
%{_libdir}/libprofiler*.so
%{_libdir}/libtcmalloc*.a
%{_libdir}/libtcmalloc*.so
%{_libdir}/pkgconfig/lib*

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*
%{_mandir}/man1/*

%changelog
* Wed Sep 13 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.10-2
- devel package should require main package
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 2.10-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.9.1-1
- Automatic Version Bump
* Fri Jul 17 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8-1
- Automatic Version Bump
* Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 2.7-1
- Update version to 2.7
* Mon Jul 31 2017 Vinay Chang Lee <changlee@vmware.com> 2.5-2
- Fix %check
* Mon Feb 06 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.5-1
- Initial version of gperftools package.
