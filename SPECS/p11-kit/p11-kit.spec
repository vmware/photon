%define _ca_trust_dir %{_sysconfdir}/pki/ca-trust

Name:           p11-kit
Summary:        Library for loading and sharing PKCS11 modules
Version:        0.24.1
Release:        2%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          Development/Libraries
License:        BSD
URL:            http://p11-glue.freedesktop.org/p11-kit.html

Source0: https://github.com/p11-glue/p11-kit/releases/download/%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=8cf170c714bb9e0cf3df93e8ec55b8e3c55cabf2c6a27f177ac6de8b8028985df2ca0216d3215d6828dc2ae3095c4e1a4febe8cb26b88ec321defc66bb011e81

Source1: update-ca-trust

BuildRequires: gcc
BuildRequires: libtasn1-devel >= 2.3
BuildRequires: libffi-devel
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: meson
BuildRequires: systemd-devel
BuildRequires: chkconfig
BuildRequires: gnupg

Requires: libffi
Requires: glibc

%description
%{name} provides a way to load and enumerate PKCS11 modules, as well
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

%package -n update-ca-trust
Summary:        Update CA trust tool
Group:          System Environment/Security
Requires:       ca-certificates
Requires:       %{name}-trust = %{version}-%{release}
Requires(post): %{name}-trust = %{version}-%{release}

%description -n update-ca-trust
Update CA trust tool

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --disable-doc-html \
    bashcompdir=%{_datadir}/bash-completion/completions

%make_build

%install
%make_install %{?_smp_mflags}

# create pkcs11 modules directory
mkdir -p %{buildroot}%{_sysconfdir}/pkcs11/modules \
         %{buildroot}%{_ca_trust_dir}/extracted/{pem,openssl,java,edk2}

cp -p %{SOURCE1} %{buildroot}%{_bindir}/update-ca-trust

mv %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf.example \
       %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf

rm -rf %{buildroot}%{_datadir}/gtk-doc

%if 0%{?with_check}
%check
%make_build check
%endif

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n update-ca-trust
%{_bindir}/update-ca-trust

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pkcs11/pkcs11.conf
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/modules
%dir %{_libexecdir}/%{name}
%{_bindir}/%{name}
%{_libdir}/libp11-kit.so.*
%{_libdir}/%{name}-proxy.so
%{_libexecdir}/%{name}/%{name}-remote
%{_datadir}/bash-completion/completions/%{name}

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}-1/
%{_libdir}/libp11-kit.so
%{_libdir}/pkgconfig/%{name}-1.pc

%files trust
%defattr(-,root,root)
%{_bindir}/trust
%dir %{_libdir}/pkcs11
%ghost %{_libdir}/libnssckbi.so
%{_libdir}/pkcs11/%{name}-trust.so
%{_datadir}/%{name}/modules/%{name}-trust.module
%{_libexecdir}/%{name}/trust-extract-compat
%{_datadir}/bash-completion/completions/trust

%files server
%defattr(-,root,root)
%{_libdir}/pkcs11/%{name}-client.so
%{_libexecdir}/%{name}/%{name}-server
%{_userunitdir}/%{name}-server.service
%{_userunitdir}/%{name}-server.socket

%files -n update-ca-trust
%defattr(-,root,root)
%{_ca_trust_dir}/*
%{_bindir}/update-ca-trust

%changelog
* Thu May 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.24.1-2
- Add update-ca-trust sub package
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 0.24.1-1
- Initial addition to Photon. Required for SSSD.
