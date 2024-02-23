Summary:        Open Source Security Compliance Solution
Name:           openscap
Version:        1.3.6
Release:        14%{?dist}
License:        GPL2+
URL:            https://www.open-scap.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/OpenSCAP/openscap/releases/download/%{version}/openscap-%{version}.tar.gz
%define sha512 %{name}=5e4d6c4addc15b2a0245b5caef80fda3020f1cac83ed4aa436ef3f1703d1d761060c931c2536fa68de7ad5bab002b79c8b2d1e5f7695d46249f4562f5a1569a0

Patch0: use-correct-includes.patch

BuildRequires:  xmlsec1-devel
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
Requires:       libxml2
Requires:       libxslt
Requires:       libselinux
Requires:       libcap
Requires:       openssl
Requires:       libgcrypt
Requires:       libacl
Requires:       pcre-libs
Requires:       xmlsec1

%description
SCAP is a multi-purpose framework of specifications that supports automated configuration,
vulnerability and patch checking, technical control compliance activities, and security measurement.
OpenSCAP has received a NIST certification for its support of SCAP 1.2.

%package        devel
Summary:        Development Libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libxml2-devel

%description    devel
Header files for doing development with %{name}.

%package        perl
Summary:        %{name} perl scripts
Requires:       perl
Requires:       %{name} = %{version}-%{release}

%description    perl
Perl scripts.

%package        python3
Summary:        %{name} python
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description    python3
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

%if 0%{?_with_check}
%check
%ctest
%endif

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_mandir}/man8/*
%{_datadir}/openscap/*
%{_libdir}/libopenscap_sce.so.*
%{_libdir}/libopenscap.so.*
%exclude %dir %{_usrsrc}/debug
%exclude %dir %{_libdir}/debug

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
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.3.6-14
- Bump version as a part of libxml2 upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.3.6-13
- Bump version as a part of openssl upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.6-12
- Bump version as a part of libxml2 upgrade
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.3.6-11
- Bump up version no. as part of swig upgrade
* Tue Jan 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.3.6-10
- Bump version as a part of rpm upgrade
* Tue Dec 06 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.6-9
- Bump version as a part of xmlsec1 upgrade
* Mon Oct 24 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.3.6-8
- Update release to compile with python 3.11
* Fri Oct 21 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.6-7
- Bump version as a part of xmlsec1 upgrade
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.6-6
- Bump version as a part of libxslt upgrade
* Sun Jul 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.6-5
- Bump version as a part of rpm upgrade
* Wed Jun 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.6-4
- Exclude debug symbols properly
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.3.6-3
- Fix build with latest cmake
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.3.6-2
- Bump version as a part of libxslt upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.6-1
- Automatic Version Bump
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 1.3.5-3
- Release bump up to use libxml2 2.9.12-1.
* Fri Aug 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.3.5-2
- Bump version as a part of rpm upgrade
* Fri Apr 23 2021 Gerrit Photon <photon-checkins@vmware.com> 1.3.5-1
- Automatic Version Bump
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
