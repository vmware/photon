Summary:        libsodium is a community accepted C library for cryptography
Name:           libsodium
Version:        1.0.18
Release:        3%{?dist}
Group:          Development/Tools
URL:            https://github.com/jedisct1/libsodium
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://download.libsodium.org/libsodium/releases/%{name}-%{version}-stable.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  gcc

%description
Sodium is a modern, easy-to-use software library for encryption,
decryption, signatures, password hashing and more.

%package    devel
Summary:    Development files for libsodium
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the header files and libraries
needed to develop applications using libsodium.

%prep
%autosetup -p1 -n %{name}-stable
%configure

%build
%make_build

%install
%make_install

%check
make check %{?_smp_mflags}

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
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/sodium/
%{_includedir}/sodium.h

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.18-3
- Release bump for SRP compliance
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.18-2
- Remove .la files
* Fri Nov 20 2020 Sharan Turlapati <sturlapati@vmware.com> 1.0.18-1
- Initial version of libsodium for Photon
