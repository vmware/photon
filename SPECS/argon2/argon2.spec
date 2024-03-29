%global libname libargon2
%global soname  1

Summary:        Tools for password hashing
Name:           argon2
Version:        20190702
Release:        3%{?dist}
License:        Apache 2.0
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/P-H-C/phc-winner-argon2

Source0: https://github.com/P-H-C/phc-winner-argon2/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=0a4cb89e8e63399f7df069e2862ccd05308b7652bf4ab74372842f66bcc60776399e0eaf979a7b7e31436b5e6913fe5b0a6949549d8c82ebd06e0629b106e85f

BuildRequires:  gcc
BuildRequires:  make

Requires: %{libname} = %{version}-%{release}
Requires: libpwquality

%description
Argon2 is a password-hashing function that summarizes the state of the art in the design of memory-hard functions and can be used to hash passwords for credential storage, key derivation, or other applications.

%package -n     %{libname}
Summary:        Argon2 password hashing library
Group:          Development/Libraries
Provides:       %{libname}.so.%{soname}()(64bit)

%description -n %{libname}
Libraries for integrating with Argon2

%package -n     %{libname}-devel
Summary:        Argon2 password hashing libraries and headers
Group:          Development/Libraries
Requires:       %{libname} = %{version}-%{release}

%description -n %{libname}-devel
Libraries and Headers for integrating with Argon2

%prep
%autosetup -p1 -n phc-winner-%{name}-%{version}

%build
%make_build LIBRARY_REL=lib OPTTARGET=%{_arch}

%install
%make_install LIBRARY_REL=lib OPTTARGET=%{_arch} \
             PREFIX=%{_prefix} %{?_smp_mflags}

rm %{buildroot}%{_libdir}/*.a
install -Dpm 644 %{libname}.pc %{buildroot}%{_libdir}/pkgconfig/%{libname}.pc

%if 0%{?with_check}
%check
make test %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}/*

%post -n %{libname}
/sbin/ldconfig

%postun -n %{libname}
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{libname}.so.%{soname}

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/%{libname}.so
%{_libdir}/pkgconfig/%{libname}.pc

%changelog
* Fri May 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 20190702-3
- Remove _isa entries
* Thu Jul 29 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 20190702-2
- Pass OPTTARGET=%{_arch} to make to avoid building package for native instruction set
* Thu Apr 8 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 20190702-1
- Initial package
