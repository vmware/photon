Summary:        libsodium is a community accepted C library for cryptography
Name:           libsodium
Version:        1.0.18
Release:        1%{?dist}
License:        ISC

Group:          Development/Tools
URL:            https://github.com/jedisct1/libsodium
Source0:        https://download.libsodium.org/libsodium/releases/%{name}-%{version}-stable.tar.gz
%define sha1 libsodium=e7a8257edc00405c365dcba79f7ac11cbac51266
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  gcc

%description
Sodium is a modern, easy-to-use software library for encryption,
decryption, signatures, password hashing and more.

%package    devel
Summary:    Development files for libsodium
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
%description devel
Summary:    This package contains the header files and libraries
	    needed to develop applications using libsodium.

%prep
%setup -q -n %{name}-stable
%configure

%build
make %{?_smp_mflags} DESTDIR=%{buildroot}

%check
make check

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_libdir}/%{name}.la
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/sodium/
%{_includedir}/sodium.h

%changelog
* Fri Nov 20 2020 Sharan Turlapati <sturlapati@vmware.com> 1.0.18-1
- Initial version of libsodium for Photon
