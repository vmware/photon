Summary:        Compressed file format
Name:           zchunk
Version:        1.2.3
Release:        2%{?dist}
License:        BSD-2-Clause AND MIT
URL:            https://github.com/zchunk/zchunk
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/zchunk/zchunk/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=5e46d8c3e36034de8424937cdfac59acdfaf332203e6e5d8b290614cbbe0340998d53b0583b0ef93189f41dc89219a75f50572757ebcea9abd83bd9aad861a73

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
Summary:    Zchunk library
Group:      System/Libraries

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
Requires:       %{name} = %{version}-%{release}
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
%autosetup
# Remove bundled sha libraries
rm -rf src/lib/hash/sha*

%build
%meson \
    -D with-openssl=enabled \
    -D with-zstd=enabled

%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_libexecdir}
install contrib/gen_xml_dictionary %{buildroot}%{_libexecdir}/zck_gen_xml_dictionary

%if 0%{?with_check}
%check
%meson_test
%endif

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md contrib
%doc LICENSE
%doc zchunk_format.txt
%{_bindir}/zck*
%{_bindir}/unzck
%{_libexecdir}/zck_gen_xml_dictionary

%files libs
%defattr(-,root,root)
%{_libdir}/libzck.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libzck.so
%{_libdir}/pkgconfig/zck.pc
%{_includedir}/zck.h
%{_mandir}/man1/*.gz

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.3-2
- Bump version as a part of openssl upgrade
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.3-1
- Upgrade to v1.2.3
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.7-2
- Bump up release for openssl
* Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.7-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.1.6-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.6-1
- Automatic Version Bump
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 1.1.1-2
- Added for ARM Build
* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.1.1-1
- Initial build. First version
