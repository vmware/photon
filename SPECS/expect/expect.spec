Summary:        Expect is a tool for automating interactive applications
Name:           expect
Version:        5.45.4
Release:        1%{?dist}
License:        GPLv2+
URL:            https://sourceforge.net/projects/expect
Source0:        https://sourceforge.net/projects/%{name}/files/Expect/%{version}/%{name}%{version}.tar.gz
%define sha1    expect=a97b2f377c6a799928d6728c2ada55beb7f57d96
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
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
%setup -q -n %{name}%{version}

%build
%configure
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*


%changelog
*   Thu Sep 20 2018 Sujay G <gsujay@vmware.com> 5.45.4-1
-   Bump expect version to 5.45.4
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-3
-   Use standard configure macros
*   Tue Aug 8 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-2
-   Fix %check section
*   Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-1
-   Initial build. First version
