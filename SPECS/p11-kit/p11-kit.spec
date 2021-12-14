Summary:      Library for loading and sharing PKCS#11 modules
Name:         p11-kit
Version:      0.24.0
Release:      1%{?dist}
License:      BSD-3-Clause
Group:        Development/Libraries/C and C++
URL:          http://p11-glue.freedesktop.org/p11-kit.html
Source0:      https://github.com/p11-glue/p11-kit/releases/download/%{version}/p11-kit-%{version}.tar.xz
%define   sha1 p11-kit=66380b519caa58d49f31f7fb4aae7b14e91b1a40
Vendor:       VMware, Inc.
Distribution: Photon

BuildRequires: gcc
BuildRequires: libtasn1-devel
BuildRequires: libffi-devel
BuildRequires: gettext
BuildRequires: meson
BuildRequires: libgpg-error-devel
BuildRequires: glib-devel
BuildRequires: gnupg
BuildRequires: systemd-devel

Requires: gnupg
Requires: glib

%description
p11-kit provides a way to load and enumerate PKCS#11 modules, as well
as a standard configuration setup for installing PKCS#11 modules in
such a way that they're discoverable.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package trust
Summary:            System trust module from %{name}
Requires:           %{name} = %{version}-%{release}

%description trust
The %{name}-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.

%package server
Summary:        Server and client commands for %{name}
Requires:       %{name} = %{version}-%{release}

%description server
The %{name}-server package contains command line tools that enable to
export PKCS#11 modules through a Unix domain socket.  Note that this
feature is still experimental.

%prep
%autosetup -p1

%build
CONFIGURE_OPTS=(
    -Dbash_completion=disabled
    -Dgtk_doc=false
    -Dman=false
    -Dtrust_paths=%{_sysconfdir}/pki/ca-trust/source:%{_datadir}/pki/ca-trust-source
)
%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

%find_lang %{name}

%check
%meson_test

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README
%dir %{_sysconfdir}/pkcs11
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%dir %{_libexecdir}/p11-kit
%{_bindir}/p11-kit
%{_libdir}/libp11-kit.so.*
%{_libdir}/p11-kit-proxy.so
%{_libexecdir}/p11-kit/p11-kit-remote
%{_sysconfdir}/pkcs11/pkcs11.conf.example

%files devel
%{_includedir}/p11-kit-1/
%{_libdir}/libp11-kit.so
%{_libdir}/pkgconfig/p11-kit-1.pc

%files trust
%{_bindir}/trust
%dir %{_libdir}/pkcs11
%ghost %{_libdir}/libnssckbi.so
%{_libdir}/pkcs11/p11-kit-trust.so
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libexecdir}/p11-kit/trust-extract-compat

%files server
%{_libdir}/pkcs11/p11-kit-client.so
%{_libexecdir}/p11-kit/p11-kit-server
%{_userunitdir}/p11-kit-server.service
%{_userunitdir}/p11-kit-server.socket

%changelog
* Tue Dec 14 2021 Susant Sahani <ssahani@vmware.com> 0.24.0-1
- Initial packaging
