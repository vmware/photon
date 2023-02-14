Name:           p11-kit
Summary:        Library for loading and sharing PKCS11 modules
Version:        0.24.1
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Libraries
License:        BSD
URL:            http://p11-glue.freedesktop.org/p11-kit.html

Source0:        https://github.com/p11-glue/p11-kit/releases/download/%{version}/p11-kit-%{version}.tar.xz
%define sha512 %{name}=8cf170c714bb9e0cf3df93e8ec55b8e3c55cabf2c6a27f177ac6de8b8028985df2ca0216d3215d6828dc2ae3095c4e1a4febe8cb26b88ec321defc66bb011e81

BuildRequires:  gcc
BuildRequires:  libtasn1-devel >= 2.3
BuildRequires:  libffi-devel
BuildRequires:  gettext
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  systemd-devel
BuildRequires:  chkconfig
BuildRequires:  gnupg

Requires: libffi
Requires: glibc

%description
p11-kit provides a way to load and enumerate PKCS11 modules, as well
as a standard configuration setup for installing PKCS11 modules in
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
Requires:           libtasn1
Requires:           nspr
Requires(post):     chkconfig
Requires(postun):   chkconfig

%description trust
The %{name}-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.

%package server
Summary:        Server and client commands for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       systemd
Requires:       xz-libs
Requires:       libcap
Requires:       util-linux-libs
Requires:       libgcrypt
Requires:       libgpg-error

%description server
The %{name}-server package contains command line tools that enable to
export PKCS11 modules through a Unix domain socket.  Note that this
feature is still experimental.

%prep
%autosetup -p1

%build
%configure --disable-static \
           --disable-doc-html \
           bashcompdir=%{_datadir}/bash-completion/completions

%make_build

%install
%make_install %{?_smp_mflags}

# create pkcs11 modules directory
mkdir -p %{buildroot}%{_sysconfdir}/pkcs11/modules

mv %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf.example %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf

rm -rf %{buildroot}%{_datadir}/gtk-doc

%if 0%{?with_check}
%check
%make_build check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pkcs11/pkcs11.conf
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%dir %{_libexecdir}/p11-kit
%{_bindir}/p11-kit
%{_libdir}/libp11-kit.so.*
%{_libdir}/p11-kit-proxy.so
%{_libexecdir}/p11-kit/p11-kit-remote
%{_datadir}/bash-completion/completions/p11-kit

%files devel
%defattr(-,root,root)
%{_includedir}/p11-kit-1/
%{_libdir}/libp11-kit.so
%{_libdir}/pkgconfig/p11-kit-1.pc

%files trust
%defattr(-,root,root)
%{_bindir}/trust
%dir %{_libdir}/pkcs11
%ghost %{_libdir}/libnssckbi.so
%{_libdir}/pkcs11/p11-kit-trust.so
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libexecdir}/p11-kit/trust-extract-compat
%{_datadir}/bash-completion/completions/trust

%files server
%defattr(-,root,root)
%{_libdir}/pkcs11/p11-kit-client.so
%{_libexecdir}/p11-kit/p11-kit-server
%{_userunitdir}/p11-kit-server.service
%{_userunitdir}/p11-kit-server.socket

%changelog
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.24.1-1
- Initial addition to Photon. Required for SSSD.
