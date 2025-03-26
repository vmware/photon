Summary:        Expect is a tool for automating interactive applications
Name:           expect
Version:        5.45.4
Release:        4%{?dist}
URL:            https://sourceforge.net/projects/expect
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://sourceforge.net/projects/%{name}/files/Expect/%{version}/%{name}%{version}.tar.gz

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
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.45.4-4
- Release bump for SRP compliance
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
