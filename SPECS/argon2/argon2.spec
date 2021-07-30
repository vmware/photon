%global libname libargon2
%global soname  1
Summary:        Tools for password hashing
Name:           argon2
Version:        20190702
Release:        2%{?dist}
License:        Apache 2.0
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    argon2=4b1de90ec1ccfb6e91001e849f2cbe0222cc8b4c
URL:            https://github.com/P-H-C/phc-winner-argon2
BuildRequires:  gcc
BuildRequires:  make
Requires:       %{libname}%{?_isa} = %{version}-%{release}
Requires:       libpwquality

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
%setup -q -n phc-winner-%{name}-%{version}

%build
# parallel build is not supported
make -j1 LIBRARY_REL=lib OPTTARGET=%{_arch}

%install
make install LIBRARY_REL=lib OPTTARGET=%{_arch} PREFIX=%{buildroot}%{_prefix}
rm %{buildroot}%{_libdir}/%{libname}.a
install -Dpm 644 %{libname}.pc %{buildroot}%{_libdir}/pkgconfig/%{libname}.pc

%check
make test

%post -n %{libname}
/sbin/ldconfig

%postun -n %{libname}
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%license LICENSE
%{_libdir}/%{libname}.so.%{soname}

%files -n %{libname}-devel
%defattr(-,root,root)
%doc *md
%{_includedir}/%{name}.h
%{_libdir}/%{libname}.so
%{_libdir}/pkgconfig/%{libname}.pc


%changelog
*   Thu Jul 29 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 20190702-2
-   Pass OPTTARGET=%{_arch} to make to avoid building package for native instruction set
*   Thu Apr 8 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 20190702-1
-   Initial package
