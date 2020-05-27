Name:           oniguruma
Version:        6.9.3
Release:        2%{?dist}
License:        BSD
Summary:        Regular expressions library
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/kkos/oniguruma/
Source0:        https://github.com/kkos/oniguruma/releases/download/v%{version}/onig-%{version}.tar.gz
%define sha1    onig=f2bde879bb7334a1b0d7b5553a851a8d6374f28b
Patch0:         oniguruma-CVE-2019-19012.patch
Patch1:         oniguruma-CVE-2019-19203.patch
Patch2:         oniguruma-CVE-2019-19204.patch
Patch3:         oniguruma-CVE-2019-19246.patch

%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)

%package devel
Summary:        Library providing headers and libraries to libonig
Group:          Development/Libraries
Requires:       oniguruma = %{version}-%{release}

%description devel
Development files for libonig

%prep
%setup -q -n onig-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure                    \
        --disable-silent-rules \
        --disable-static       \
        --with-rubydir=%{_bindir}
make

%install
make install \
        DESTDIR=%{buildroot}  \
        INSTALL="install -c -p"
find %{buildroot}/%{_libdir} -name '*.la' -delete

%check
make  check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libonig.so.*

%files devel
%defattr(-,root,root,-)
%doc    AUTHORS
%license        COPYING
%doc    README
%doc    index.html
%lang(ja)       %doc    README_japanese
%lang(ja)       %doc    index_ja.html
%{_bindir}/onig-config
%{_libdir}/libonig.so
%{_includedir}/onig*.h
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Dec 13 2019 Dweep Advani <dadvani@vmware.com> 6.9.3-2
- Fixing CVE-2019-19012, CVE-2019-1920[34] and CVE-2019-19246
* Wed Sep 18 2019 Dweep Advani <dadvani@vmware.com> 6.9.3-1
- Upgrading to 6.9.3 for fixing CVE-2019-13225 and CVE-2019-16163
* Mon Jul 15 2019 Dweep Advani <dadvani@vmware.com> 6.9.0-2
- Fixed CVE-2019-13224
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.9.0-1
- Upgrade to 6.9.0
- Created devel package
* Tue Aug 22 2017 Chang Lee <changlee@vmware.com> 6.5.0-1
- Initial version
