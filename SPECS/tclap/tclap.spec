Summary:      simple interface for defining and acessing commandline arguments
Name:         tclap
Version:      1.2.5
Release:      1%{?dist}
License:      MIT
URL:          http://tclap.sourceforge.net
Group:        Development/Libraries
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha512  tclap=3b5b3d76e8ff21133001f5f9589fa6ec143729909bf0b9cc9934377bce178360c161fb5c1f4c4d9e9c74b09cff3d65f1d5100e61d4a732283524a78b6f236b10
BuildArch:    noarch

%description
TCLAP is a small, flexible library that provides a simple interface for defining and accessing command line
arguments. It was intially inspired by the user friendly CLAP libary. The difference is that this library is
templatized, so the argument class is type independent. Type independence avoids identical-except-for-type
objects, such as IntArg, FloatArg, and StringArg. While the library is not strictly compliant with the GNU
or POSIX standards, it is close.

%package      doc
Summary:      API Documentation for tclap
Group:        Documentation

%description  doc
API documentation for TCLAP

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
make check %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%files doc
%defattr(-,root,root)
%{_docdir}/*

%changelog
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.5-1
-   Automatic Version Bump
*   Thu May 06 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.4-1
-   Automatic Version Bump
*   Wed Sep 23 2020 Michelle Wang <michellew@vmware.com> 1.2.2-3
-   Fix spec configuration
*   Tue Jan 08 2019 Michelle Wang <michellew@vmware.com> 1.2.2-2
-   Fix make check for tclap.
*   Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.2.2-1
-   Update version to 1.2.2.
*   Tue Jun 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-1
-   First version.
