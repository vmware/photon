Summary:        A library implementing the SSH protocol
Name:           libssh
Version:        0.9.6
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/NetworkingLibraries
URL:            https://www.libssh.org
Source0:        https://www.libssh.org/files/0.9/%{name}-%{version}.tar.xz
%define sha1    libssh=1b2dd673b58e1eaf20fde45cd8de2197cfab2f78
Source3:        libssh_client.config
Source4:        libssh_server.config
BuildRequires:  build-essential
BuildRequires:  cmake
BuildRequires:  krb5-devel
BuildRequires:  nmap-ncat
BuildRequires:  openssh-clients
BuildRequires:  openssh-server
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  libpcap-devel
Requires:       %{name}-config = %{version}-%{release}
Requires:       e2fsprogs-libs
Requires:       krb5

%description
The ssh library was designed to be used by programmers needing a working SSH
implementation by the mean of a library. The complete control of the client is
made by the programmer. With libssh, you can remotely execute programs, transfer
files, use a secure and transparent tunnel for your remote programs. With its
Secure FTP implementation, you can play with remote files easily, without
third-party programs others than libcrypto (from openssl).

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package config
Summary:        Configuration files for %{name}
BuildArch:      noarch

%description config
The %{name}-config package provides the default configuration files for %{name}.

%prep
%autosetup -p1

%build
mkdir build
pushd build
cmake .. \
         -DCMAKE_BUILD_TYPE=Release \
         -DBUILD_SHARED_LIBS=ON \
         -DJSONCPP_WITH_WARNING_AS_ERROR=OFF \
         -DJSONCPP_WITH_PKGCONFIG_SUPPORT=ON \
         -DJSONCPP_WITH_POST_BUILD_UNITTEST=OFF \
         -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
         -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
         -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
         -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
         -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
         -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
         -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
         -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
         -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
         -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
         -DGLOBAL_CLIENT_CONFIG="%{_sysconfdir}/libssh/libssh_client.config" \
         -DGLOBAL_BIND_CONFIG="%{_sysconfdir}/libssh/libssh_server.config"
make %{?_smp_mflags}
popd

%install
pushd build
make install DESTDIR=%{buildroot} %{?_smp_mflags}
install -d -m755 %{buildroot}%{_sysconfdir}/libssh
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/libssh/libssh_client.config
install -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/libssh/libssh_server.config
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
ctest --output-on-failure

%files
%doc AUTHORS BSD ChangeLog README
%license COPYING
%{_libdir}/libssh.so.4*

%files devel
%{_includedir}/libssh/
%dir %{_libdir}/cmake/
%{_libdir}/cmake/libssh/
%{_libdir}/pkgconfig/libssh.pc
%{_libdir}/libssh.so

%files config
%attr(0755,root,root) %dir %{_sysconfdir}/libssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/libssh/libssh_client.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/libssh/libssh_server.config

%changelog
* Wed Jan 12 2022 Tapas Kundu <tkundu@vmware.com> - 0.9.6-1
- Initial packaging to photon distro
