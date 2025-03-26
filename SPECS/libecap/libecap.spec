Summary:      Squid interface for embedded adaptation modules
Name:         libecap
Version:      1.0.1
Release:      2%{?dist}
URL:          http://www.e-cap.org/
Source0:      http://www.e-cap.org/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Group:        System Environment/Base
Vendor:       VMware, Inc.
Distribution: Photon

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
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the libraries, include files, and other
resources needed for developing libecap applications.

%prep
%autosetup

%build
%configure

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -f %{buildroot}%{_libdir}/libecap.a
rm -f %{buildroot}%{_libdir}/libecap.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE CREDITS NOTICE README
%{_libdir}/libecap.so.*

%files devel
%{_libdir}/libecap.so
%{_libdir}/pkgconfig/libecap.pc
%{_includedir}/libecap

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.1-2
- Release bump for SRP compliance
* Fri Apr 30 2021 Susant Sahani <ssahani@vmware.com> 1.0.1-1
- Initial rpm release.
