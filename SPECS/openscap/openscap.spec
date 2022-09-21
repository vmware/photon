Summary:        Open Source Security Compliance Solution
Name:           openscap
Version:        1.3.4
Release:        7%{?dist}
License:        GPL2+
URL:            https://www.open-scap.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/OpenSCAP/openscap/releases/download/%{version}/openscap-%{version}.tar.gz
%define sha512 %{name}=686dbae35fa7b3a3fcb05b0e8babc15249b1830b61388d57b4107507c3a133b9c87a8d32bdd7a796c2726f13774a706b8ed0c9bab158f98eaebec7859fc96755

BuildRequires:  swig
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  XML-Parser
BuildRequires:  rpm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  pcre-devel
BuildRequires:  libacl-devel
BuildRequires:  libselinux-devel
BuildRequires:  libcap-devel
BuildRequires:  util-linux-devel
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  popt-devel
BuildRequires:  python3-devel
BuildRequires:  cmake

Requires:       curl
Requires:       popt

%description
SCAP is a multi-purpose framework of specifications that supports automated configuration, vulnerability and patch checking, technical control compliance activities, and security measurement.
OpenSCAP has received a NIST certification for its support of SCAP 1.2.

%package devel
Summary: Development Libraries for openscap
Group: Development/Libraries
Requires: openscap = %{version}-%{release}
Requires: libxml2-devel

%description devel
Header files for doing development with openscap.

%package perl
Summary: openscap perl scripts
Requires: perl
Requires: openscap = %{version}-%{release}

%description perl
Perl scripts.

%package python3
Summary: openscap python
Group: Development/Libraries
Requires: openscap = %{version}-%{release}

%description python3
Python bindings.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    -DENABLE_PERL=ON \
    -DENABLE_SCE=ON

%cmake_build

%install
%cmake_install
find %{buildroot} -name '*.la' -delete

%if 0%{?_with_check}
%check
ctest -V %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%exclude %dir %{_usrsrc}/debug
%exclude %dir %{_libdir}/debug
%{_bindir}/*
%{_mandir}/man8/*
%{_datadir}/openscap/*
%{_datadir}/perl5/*
%{_libdir}/libopenscap_sce.so.*
%{_libdir}/libopenscap.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libopenscap_sce.so
%{_libdir}/libopenscap.so
%{_libdir}/pkgconfig/*

%files perl
%defattr(-,root,root)
%{_libdir}/perl5/*

%files python3
%defattr(-,root,root)
%{_libdir}/python%{python3_version}/*

%changelog
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.4-7
- Exclude debug symbols properly
* Mon Nov 22 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.3.4-6
- Update release to compile with python 3.10
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.3.4-5
- Release bump up to use libxml2 2.9.12-1.
* Thu Nov 11 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.3.4-4
- Bump version as a part of rpm upgrade
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 1.3.4-3
- Replacement of ITS suggested words.
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 1.3.4-2
- Build with python3
* Thu Oct 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.4-1
- Automatic Version Bump
* Mon Jul 27 2020 Vikash Bansal <bvikas@vmware.com> 1.3.3-1
- Update to 1.3.3
* Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 1.2.17-3
- Build with python 3.8
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 1.2.17-2
- Mass removal python2
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.2.17-1
- Update to 1.2.17
* Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.14-3
- Deactivate make check which need per-XML-XPATH for bug 1900358
* Fri May 5 2017 Alexey Makhalov <amakhalov@vmware.com> 1.2.14-2
- Remove BuildRequires XML-XPath.
* Mon Mar 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.14-1
- Update to latest version.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-2
- BuildRequires curl-devel.
* Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-1
- Initial build. First version
