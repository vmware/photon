Summary:        iSNS server and client for Linux
Name:           open-isns
Version:        0.101
Release:        4%{?dist}
License:        LGPLv2.1
URL:            https://github.com/open-iscsi/open-isns
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.gz
%define sha512 open=e5a392127b0d85f36e9e4aa963c0c502af8c5aea0aba6d12abb4425649969dcc20ba6e87a99083626d981438439b17b71a86320f816042d82ed5dbe7e7a63e77

BuildRequires: systemd-devel
BuildRequires: openssl-devel

Requires: openssl-libs
Requires: systemd

%description
iSNS server and client for Linux

%package devel
Summary:    Development Libraries for open-isns
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Header files for doing development with open-isns.

%prep
%autosetup -p1

%build
export CFLAGS="-Werror=unused-result"

%configure \
  --disable-static \
  --enable-shared

%make_build

%install
%make_install %{?_smp_mflags} install_hdrs install_lib

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/isns/isns*.conf
%{_libdir}/*.so.*
%{_unitdir}/isnsd.service
%{_unitdir}/isnsd.socket
%{_sbindir}/isns*
%{_mandir}/man5/*.gz
%{_mandir}/man8/*.gz

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/libisns/*.h

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.101-4
- Bump version as a part of openssl upgrade
* Thu Oct 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.101-3
- Fix spec issues
* Mon Nov 15 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.101-2
- Increment for openssl 3.0.0 compatibility
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 0.101-1
- Initial version.
