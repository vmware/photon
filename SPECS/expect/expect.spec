Summary:        Expect is a tool for automating interactive applications
Name:           expect
Version:        5.45.4
Release:        3%{?dist}
URL:            https://sourceforge.net/projects/expect
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://sourceforge.net/projects/%{name}/files/Expect/%{version}/%{name}%{version}.tar.gz
%define sha512  %{name}=a8dc25e8175f67e029e15cbcfca1705165c1c4cb2dd37eaaaebffb61e3ba132d9519cd73ca5add4c3358a2b0b7a91e878279e8d0b72143ff2c287fce07e4659a

Source1: license.txt
%include %{SOURCE1}

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
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
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
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.45.4-3
- Release bump for SRP compliance
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.45.4-2
- Fix binary path
* Thu Sep 20 2018 Sujay G <gsujay@vmware.com> 5.45.4-1
- Bump expect version to 5.45.4
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-3
- Use standard configure macros
* Tue Aug 8 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-2
- Fix %check section
* Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 5.45-1
- Initial build. First version
