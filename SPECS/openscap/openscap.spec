Summary:        Open Source Security Compliance Solution
Name:           openscap
Version:        1.2.17
Release:        1%{?dist}
License:        GPL2+
URL:            https://www.open-scap.org
Source0:        https://github.com/OpenSCAP/openscap/releases/download/%{version}/openscap-%{version}.tar.gz
%define sha1    openscap=588676a56b6adf389140d6fdbc6a6685ef06e7b3
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
BuildRequires:  python2-devel
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

%package python
Summary: openscap python
Group: Development/Libraries
Requires: openscap = %{version}-%{release}
BuildRequires:  python2-devel
%description python
Python bindings.


%prep
%setup -q
%build
./configure --prefix=/usr \
            --sysconfdir=/etc \
            --enable-sce \
            --enable-perl
make
%install
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
%{_libexecdir}/*
%{_mandir}/man8/*
/usr/share/openscap/*
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

%files python
%defattr(-,root,root)
%{_libdir}/python2.7/*

%changelog
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
