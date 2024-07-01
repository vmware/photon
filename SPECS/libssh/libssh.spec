Summary:        A library implementing the SSH protocol
Name:           libssh
Version:        0.10.5
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/NetworkingLibraries
URL:            https://www.libssh.org

Source0: https://www.libssh.org/files/0.10/%{name}-%{version}.tar.xz
%define sha512 %{name}=2b758f9df2b5937865d4aee775ffeafafe3ae6739a89dfc470e38c7394e3c3cb5fcf8f842fdae04929890ee7e47bf8f50e3a38e82dfd26a009f3aae009d589e0

Source1: libssh_client.config
Source2: libssh_server.config

BuildRequires: build-essential
BuildRequires: cmake
BuildRequires: krb5-devel
BuildRequires: nmap-ncat
BuildRequires: openssh-clients
BuildRequires: openssh-server
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: libpcap-devel

Requires: %{name}-config = %{version}-%{release}
Requires: e2fsprogs-libs
Requires: krb5

%description
The ssh library was designed to be used by programmers needing a working SSH
implementation by the mean of a library. The complete control of the client is
made by the programmer. With %{name}, you can remotely execute programs, transfer
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
%cmake \
     -DCMAKE_BUILD_TYPE=Debug \
     -DBUILD_SHARED_LIBS=ON \
     -DJSONCPP_WITH_WARNING_AS_ERROR=OFF \
     -DJSONCPP_WITH_PKGCONFIG_SUPPORT=ON \
     -DJSONCPP_WITH_POST_BUILD_UNITTEST=OFF \
     -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
     -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
     -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
     -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
     -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
     -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
     -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
     -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
     -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
     -DGLOBAL_CLIENT_CONFIG="%{_sysconfdir}/%{name}/%{name}_client.config" \
     -DGLOBAL_BIND_CONFIG="%{_sysconfdir}/%{name}/%{name}_server.config"

%cmake_build

%install
%cmake_install
install -d -m755 %{buildroot}%{_sysconfdir}/%{name}
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/%{name}_client.config
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/%{name}_server.config

%ldconfig_scriptlets

%if 0%{?with_check}
%check
%ctest
%endif

%files
%defattr(-,root,root)
%doc AUTHORS BSD README
%license COPYING
%{_libdir}/%{name}.so.4*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/
%dir %{_libdir}/cmake/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%files config
%defattr(-,root,root)
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}_client.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}_server.config

%changelog
* Mon Jul 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.10.5-3
- Bump version as a part of openssh upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.10.5-2
- Bump version as a part of openssl upgrade
* Tue Sep 05 2023 Nitesh Kumar <kunitesh@vmware.com> 0.10.5-1
- Version upgrade to v0.10.5 to fix follwing CVE's:
- CVE-2023-2023-1667, CVE-2023-2283
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 0.9.6-5
- Bump version as a part of krb5 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.9.6-4
- Bump version as a part of zlib upgrade
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.9.6-3
- Bump version as a part of krb5 upgrade
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.9.6-2
- Use cmake macros for build
* Wed Jan 12 2022 Tapas Kundu <tkundu@vmware.com> 0.9.6-1
- Initial packaging to photon distro
