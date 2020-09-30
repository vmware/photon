Summary:        Compressed file format
Name:           zchunk
Version:        1.1.7
Release:        1%{?dist}
License:        BSD-2-Clause AND MIT
URL:            https://github.com/zchunk/zchunk
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/zchunk/zchunk/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=92a940280b2e9981f5d8547158a6c80aa3bfa6be
BuildRequires:  meson
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
Requires:       %{name}-libs = %{version}-%{release}

%description
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

%package libs
Summary:        Zchunk library
Group:          System/Libraries

%description libs
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the zchunk library, libzck.

%package devel
Summary:        Headers for building against zchunk
Group:          Development/Libraries/C and C++
Requires:       %{name}-libs = %{version}-%{release}

%description devel
zchunk is a compressed file format that splits the file into independent
chunks.  This allows you to only download the differences when downloading a
new version of the file, and also makes zchunk files efficient over rsync.
zchunk files are protected with strong checksums to verify that the file you
downloaded is in fact the file you wanted.

This package contains the headers necessary for building against the zchunk
library, libzck.

%prep
%setup -q
# Remove bundled sha libraries
rm -rf src/lib/hash/sha*

%build
mkdir build &&
cd build &&
meson --prefix=%{_prefix} -Dwith-openssl=enabled .. &&
ninja

%install
cd build
DESTDIR=%{buildroot}/ ninja install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md contrib
%doc LICENSE
%doc zchunk_format.txt
%{_bindir}/zck*
%{_bindir}/unzck

%files libs
%{_libdir}/libzck.so.*

%files devel
%{_libdir}/libzck.so
%{_libdir}/pkgconfig/zck.pc
%{_includedir}/zck.h
%{_mandir}/man1/*.gz

%changelog
*   Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.7-1
-   Automatic Version Bump
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.6-2
-   openssl 1.1.1
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.6-1
-   Automatic Version Bump
*   Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 1.1.1-2
-   Added for ARM Build
*   Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.1.1-1
-   Initial build. First version
