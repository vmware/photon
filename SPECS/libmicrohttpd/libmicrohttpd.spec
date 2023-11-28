Name:           libmicrohttpd
Summary:        Lightweight library for embedding a webserver in applications
Version:        0.9.76
Release:        2%{?dist}
License:        LGPLv2+
URL:            http://www.gnu.org/software/libmicrohttpd/
Source0:        https://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
%define sha512  %{name}=9ff8a837892142376eaeaf50c0b0dba76697d0ff44b908434cba8db4324c57dfb8bbcc1a922b97d825891ac10f50693dee9388531856e0fa81fa2cfeac538581
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  autoconf, automake, libtool
BuildRequires:  gnutls-devel

Requires:       gnutls

%description
GNU libmicrohttpd is a small C library that is supposed to make it
easy to run an HTTP server as part of another application.

%package devel
Summary:        Development files for libmicrohttpd
Requires:       %{name} = %{version}-%{release}
Requires:       gnutls-devel
%description devel
Development files for libmicrohttpd

%prep
%autosetup -p1

%build
%configure --disable-static --with-gnutls --enable-https=yes
%make_build

%install
%make_install %{?_smp_mflags}

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_bindir}/demo

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libmicrohttpd.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/microhttpd.h
%{_libdir}/libmicrohttpd.so
%{_libdir}/pkgconfig/libmicrohttpd.pc

%{_datadir}/info/libmicrohttpd-tutorial.info.gz
%{_datadir}/info/libmicrohttpd.info.gz
%{_datadir}/info/libmicrohttpd_performance_data.png.gz
%{_datadir}/man/man3/libmicrohttpd.3.gz

%changelog
* Tue Nov 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.9.76-2
- Bump version as a part of gnutls upgrade
* Fri Apr 28 2023 Ankit Jain <ankitja@vmware.com> 0.9.76-1
- Updated to v0.9.76
* Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> 0.9.71-2
- Requires gnutls-devel for installation
* Fri Aug 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.9.71-1
- Automatic Version Bump
* Wed Aug 12 2020 Susant Sahani <ssahani@vmware.com> 0.9.70-1
- Initial rpm release
