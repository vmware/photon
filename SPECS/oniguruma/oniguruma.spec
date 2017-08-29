Name:           oniguruma
Version:        6.5.0
Release:        1%{?dist}
Summary:        Regular expressions library
Group:          System Environment/Libraries
License:        BSD
URL:            https://github.com/kkos/oniguruma/
Source0:        https://github.com/kkos/oniguruma/releases/download/v%{version}/onig-%{version}.tar.gz
%define sha1    onig=1347cc424b8b631b3fe9b7972b27c797a0ffdd3e
%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)

%prep
%setup -q -n onig-%{version}
%build
./configure                    \
        --prefix=%{_prefix}    \
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
%defattr(-,root,root,-)
%doc    AUTHORS
%license        COPYING
%doc    README
%doc    index.html
%lang(ja)       %doc    README.ja
%lang(ja)       %doc    index_ja.html
%{_bindir}/onig-config
%{_libdir}/libonig.so
%{_libdir}/libonig.so.4*
%{_includedir}/onig*.h
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Aug 22 2017 Chang Lee <changlee@vmware.com> 6.5.0-1
- Initial version
