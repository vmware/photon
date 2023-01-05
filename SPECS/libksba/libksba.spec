Summary:    Library for accessing X.509 and CMS data structure.
Name:       libksba
Version:    1.6.2
Release:    3%{?dist}
License:    GPLv3+
URL:        https://www.gnupg.org/(fr)/download/index.html#libksba
Group:      Security/Libraries.
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=50533887942921f8009cedd636915c2b27f231151a3b8316af6801a5f8637d66896ba5a24207bf82d8b03e26624133e80c6dd69f1196f06ada929090ef0f178c

BuildRequires: libgpg-error-devel >= 1.2

Requires: libgpg-error

Patch0: Fix-for-CVE-2022-47629.patch

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
%make_build %{?_smp_mflags}

%install
%{make_install} %{?_smp_mflags}
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
* Thu Jan 05 2023 Srish Srinivasan <ssrish@vmware.com> 1.6.2-3
- Fix for CVE-2022-47629
* Thu Dec 22 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.6.2-2
- Bump release as a part of libgpg-error upgrade to 1.46
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.2-1
- Automatic Version Bump
* Tue May 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-2
- Fix packaging, add devel sub package
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.5.1-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.3.5-1
- Udpated to version 1.3.5
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
- BuildRequired libgpg-error-devel.
* Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 1.3.4-1
- Initial Build.
