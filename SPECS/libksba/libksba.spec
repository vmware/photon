Summary:    Library for accessing X.509 and CMS data structure.
Name:       libksba
Version:    1.4.0
Release:    4%{?dist}
License:    GPLv3+
URL:        https://www.gnupg.org/(fr)/download/index.html#libksba
Group:      Security/Libraries.
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=7c1666017ebfa50b5663153dead1e019e0ee342c4f44ee8f644fc749e82dcc983237ef0f557de9de3f7908dc90405d967a4db2e36e04fe0d5a09edf49f8a0c8d

BuildRequires: libgpg-error-devel >= 1.2

Requires: libgpg-error

Patch0: 0001-Fix-for-CVE-2022-47629.patch
# Fix for CVE-2022-3515
Patch1: 0001-Detect-a-possible-overflow-directly-in-the-TLV-parse.patch

%description
Libksba is a library to make the tasks of working with X.509 certificates,
CMS data and related objects more easy. It provides a highlevel interface
to the implemented protocols and presents the data in a consistent way.

%package devel
Summary: Development headers and libraries for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
%{summary}.

%prep
%autosetup -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete
rm %{buildroot}%{_infodir}/dir

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/ksba-config

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_infodir}/ksba.info.gz
%{_datadir}/aclocal/ksba.m4
%{_libdir}/pkgconfig/ksba.pc

%changelog
* Sun Jan 22 2023 Srish Srinivasan <ssrish@vmware.com> 1.4.0-4
- Fix for CVE-2022-3515
* Thu Jan 05 2023 Srish Srinivasan <ssrish@vmware.com> 1.4.0-3
- Fix for CVE-2022-47629
* Tue May 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-2
- Fix packaging, add devel sub package
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.3.5-1
- Udpated to version 1.3.5
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
- BuildRequired libgpg-error-devel.
* Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 1.3.4-1
- Initial Build.
