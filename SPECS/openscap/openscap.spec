Summary:        Open Source Security Compliance Solution
Name:           openscap
Version:        1.3.3
Release:        1%{?dist}
License:        GPL2+
URL:            https://www.open-scap.org
Source0:        https://github.com/OpenSCAP/openscap/releases/download/%{version}/openscap-%{version}.tar.gz
%define sha1    openscap=6988d1ea7b86669d410ab5defc1be394cba5b017
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  swig libxml2-devel libxslt-devel XML-Parser
BuildRequires:  rpm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  pcre-devel
BuildRequires:  libacl-devel
BuildRequires:  libselinux-devel libcap-devel
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
%setup -q
%build
mkdir build && cd build
cmake \
-DCMAKE_BUILD_TYPE=Debug \
-DCMAKE_INSTALL_PREFIX=%{_prefix} \
-DCMAKE_INSTALL_LIBDIR:PATH=lib \
--enable-sce \
--enable-perl \
..

make

%install
cd build
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

#%check
#make check need BuildRequires per-XML-XPATH and bzip2
#no per-XML-XPATH so disable make check
#make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%exclude /usr/src/debug
%exclude %{_libdir}/debug
%{_bindir}/*
%{_mandir}/man8/*
/usr/share/openscap/*
/usr/share/perl5/*
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
%{_libdir}/python3.8/*

%changelog
*   Mon Jul 27 2020 Vikash Bansal <bvikas@vmware.com> 1.3.3-1
-   Update to 1.3.3
*   Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 1.2.17-3
-   Build with python 3.8
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 1.2.17-2
-   Mass removal python2
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.2.17-1
-   Update to 1.2.17
*   Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.14-3
-   Disable make check which need per-XML-XPATH for bug 1900358
*   Fri May 5 2017 Alexey Makhalov <amakhalov@vmware.com> 1.2.14-2
-   Remove BuildRequires XML-XPath.
*   Mon Mar 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.14-1
-   Update to latest version.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-2
-   BuildRequires curl-devel.
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-1
-   Initial build. First version
