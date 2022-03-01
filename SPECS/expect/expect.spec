Summary:        Expect is a tool for automating interactive applications
Name:           expect
Version:        5.45.4
Release:        2%{?dist}
License:        GPLv2+
URL:            https://sourceforge.net/projects/expect
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://sourceforge.net/projects/%{name}/files/Expect/%{version}/%{name}%{version}.tar.gz
%define sha1    %{name}=a97b2f377c6a799928d6728c2ada55beb7f57d96

Requires:       tcl

BuildRequires:  tcl-devel

%description
Expect is a tool for automating interactive applications such as
telnet, ftp, passwd, fsck, rlogin, tip, etc. Expect is also useful
for testing these same applications.

%package devel
Summary: Headers and development libraries for expect
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: tcl-devel

%description devel
Headers and development libraries for expect

%prep
%autosetup -p1 -n %{name}%{version}

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/%{name}%{version}/*
%exclude %dir %{_libdir}/debug
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.45.4-2
- Exclude debug symbols properly
* Thu Sep 20 2018 Sujay G <gsujay@vmware.com> 5.45.4-1
- Bump expect version to 5.45.4
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-3
- Use standard configure macros
* Tue Aug 8 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-2
- Fix %check section
* Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-1
- Initial build. First version
