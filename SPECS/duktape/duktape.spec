Name:       duktape
Version:    2.7.0
Release:    2%{?dist}
Summary:    Embeddable Javascript engine
Vendor:     VMware, Inc.
Group:      Development/Tools
URL:        http://duktape.org
Distribution: Photon

Source0:        http://duktape.org/%{name}-%{version}.tar.xz
%define sha512 %{name}=8ff5465c9c335ea08ebb0d4a06569c991b9dc4661b63e10da6b123b882e7375e82291d6b883c2644902d68071a29ccc880dae8229447cebe710c910b54496c1d

Source1:        duktape.pc.in

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  gcc
BuildRequires:  make

%description
Duktape is an embeddable Javascript engine, with a focus on portability and
compact footprint.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
Embeddable Javascript engine.

This package contains header files and libraries needed to develop
application that use %{name}.

%prep
%autosetup -p1

sed -e's|@prefix@|%{_prefix}|' \
    -e's|@libdir@|%{_lib}|' \
    -e's|@PACKAGE_VERSION@|%{version}|' \
    < %{SOURCE1} > %{name}.pc.in

mv Makefile.sharedlibrary Makefile

%build
if false; then
sed -e '/^INSTALL_PREFIX/s|[^=]*$|%{_prefix}|' \
    -e '/install\:/a\\tinstall -d $(DESTDIR)$(INSTALL_PREFIX)/%{_lib}\n\tinstall -d $(DESTDIR)$(INSTALL_PREFIX)/include' \
    -e 's/\(\$.INSTALL_PREFIX.\)/$(DESTDIR)\1/g' \
    -e 's/\/lib\b/\/%{_lib}/g' \
    < Makefile.sharedlibrary > Makefile
fi

%make_build

%install
export INSTALL_PREFIX=%{_prefix}
%make_install %{?_smp_mflags}

install -Dm0644 %{name}.pc.in %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE.txt
%doc AUTHORS.rst
%{_libdir}/libduktape.so.*
%{_libdir}/libduktaped.so.*

%files devel
%defattr(-,root,root)
%doc examples/ README.rst
%{_includedir}/duk_config.h
%{_includedir}/duktape.h
%{_libdir}/libduktape.so
%{_libdir}/libduktaped.so
%{_libdir}/pkgconfig/duktape.pc

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.7.0-2
- Release bump for SRP compliance
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.7.0-1
- First build. Needed by polkit.
