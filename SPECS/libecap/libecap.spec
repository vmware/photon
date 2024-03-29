Summary:      Squid interface for embedded adaptation modules
Name:         libecap
Version:      1.0.1
Release:      2%{?dist}
License:      BSD
URL:          http://www.e-cap.org
Group:        System Environment/Base
Vendor:       VMware, Inc.
Distribution: Photon

Source0: http://www.e-cap.org/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=0054ad11b3f558d7c623060a69207a1b8e679803cabdf1a2bce4b04335d71c016eec770fc9d2cbf3d0a93502c255cb528305f9f8e6df4e095fcb980667045919

%description
eCAP is a software interface that allows a network application, such as an
HTTP proxy or an ICAP server, to outsource content analysis and adaptation to
a loadable module. For each applicable protocol message being processed, an
eCAP-enabled host application supplies the message details to the adaptation
module and gets back an adapted message, a "not interested" response, or a
"block this message now!" instruction. These exchanges often include message
bodies.

The adaptation module can also exchange meta-information with the host
application to supply additional details such as configuration options, a
reason behind the decision to ignore a message, or a detected virus name.

If you are familiar with the ICAP protocol (RFC 3507), then you may think of
eCAP as an "embedded ICAP", where network interactions with an ICAP server are
replaced with function calls to an adaptation module.

%package devel
Summary:    Libraries and header files for the libecap library
Requires:   %{name} = %{version}-%{release}

%description devel
This package provides the libraries, include files, and other
resources needed for developing libecap applications.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
rm %{buildroot}%{_libdir}/libecap.a

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libecap.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libecap.so
%{_libdir}/pkgconfig/libecap.pc
%{_includedir}/libecap

%changelog
* Fri May 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0.1-2
- Remove _isa entries
* Fri Apr 30 2021 Susant Sahani <ssahani@vmware.com> 1.0.1-1
- Initial rpm release.
