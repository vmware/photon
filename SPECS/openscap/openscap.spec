Summary:        Open Source Security Compliance Solution
Name:           openscap
Version:        1.2.10
Release:        1%{?dist}
License:        GPL2+
URL:            https://www.open-scap.org
Source0:        https://github.com/OpenSCAP/openscap/releases/download/%{version}/openscap-%{version}.tar.gz
%define sha1    openscap=d75375b87afa7032de659ee36258caf2bc6a2b7f
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
#BuildArch:     noarch
BuildRequires:  swig libxml2-devel libxslt-devel XML-Parser
BuildRequires:  rpm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  pcre-devel
BuildRequires:  libacl-devel
BuildRequires:  libselinux-devel libcap-devel
BuildRequires:  util-linux-devel
BuildRequires:  bzip2-devel
BuildRequires:  XML-XPath
BuildRequires:  curl
BuildRequires:  popt-devel
BuildRequires:  python2-devel
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
find %{buildroot} -name '*.la' -delete

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
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-1
-   Initial build. First version
