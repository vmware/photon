Name:           oniguruma
Version:        6.9.8
Release:        1%{?dist}
License:        BSD
Summary:        Regular expressions library
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/kkos/oniguruma/
Source0:        https://github.com/kkos/oniguruma/releases/download/v%{version}/onig-%{version}.tar.gz
%define sha512    onig=6f541e8cecf73b029e54d4e11a6ddffe058d6c47674086df5a3921323351032819aca2719d35584648c3bffce6779d976a7513eabd4645362b3af701e59c67ca
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
%autosetup

%build
autoreconf -vfi
%configure                    \
        --disable-silent-rules \
        --disable-static       \
        --with-rubydir=%{_bindir}
make %{?_smp_mflags}

%install
make install %{?_smp_mflags} \
        DESTDIR=%{buildroot}  \
        INSTALL="install -c -p"
find %{buildroot}/%{_libdir} -name '*.la' -delete

%check
make check %{?_smp_mflags}
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
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 6.9.8-1
- Automatic Version Bump
* Wed Apr 14 2021 Gerrit Photon <photon-checkins@vmware.com> 6.9.7-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 6.9.6-1
- Automatic Version Bump
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 6.9.5-1
- Automatic Version Bump
* Mon Jul 15 2019 Dweep Advani <dadvani@vmware.com> 6.9.0-2
- Fixed CVE-2019-13224
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 6.9.0-1
- Upgrade to 6.9.0
- Created devel package
* Tue Aug 22 2017 Chang Lee <changlee@vmware.com> 6.5.0-1
- Initial version
