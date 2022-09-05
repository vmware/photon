Name:         erlang
Summary:      erlang
Version:      24.3.4.5
Release:      1%{?dist}
Group:        Development/Languages
Vendor:       VMware, Inc.
Distribution: Photon
License:      ASL2.0
URL:          http://erlang.com

Source0:      OTP-%{version}.tar.gz
%define sha512  OTP=7f9826be5d5afd9d9adaaebdb55165e536c5d2efaa4bbd11cb826bf255b2d89feac8abe5a805bf7ad717fdd0c1633ea2e12692366e2d38fcb8c3d0c452ae17cd
Requires:   ncurses-libs
BuildRequires: unzip
%description
erlang programming language

%prep
%autosetup -p1 -n otp-OTP-%{version}

%build
export ERL_TOP=${PWD}
./otp_build autoconf
sh ./configure --disable-hipe --prefix=%{_prefix} --enable-fips
%make_build

%install
%make_install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/%{name}/*
%exclude %dir %{_usrsrc}
%exclude %dir %{_libdir}/debug

%changelog
* Mon Sep 05 2022 Harinadh D <hdommaraju@vmware.com> 24.3.4.5-1
- Version update
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 23.1-4
- Exclude debug symbols properly
* Thu Dec 16 2021 Nitesh Kumar <kunitesh@vmware.com> 23.1-3
- Enable FIPS, Adding ncurses-libs as Requires.
* Thu May 06 2021 Harinadh D <hdommaraju@vmware.com> 23.1-2
- Fix CVE-2021-29221
* Wed Nov 11 2020 Harinadh D <hdommaraju@vmware.com> 23.1-1
- Update to version 23-1 and make compatible with rabbitmq 3.8.x
* Tue Oct 29 2019 Keerthana K <keerthanak@vmware.com> 22.1-1
- Update to latest version 22.1
* Thu Jan 31 2019 Siju Maliakkal <smaliakkal@vmware.com> 19.3-3
- Revert to old version to fix rabbitmq-server startup failure
* Fri Dec 07 2018 Ashwin H <ashwinh@vmware.com> 21.1.4-1
- Update to version 21.1.4
* Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 21.0-1
- Update to version 21.0
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 19.3-2
- Remove BuildArch
* Thu Apr 06 2017 Chang Lee <changlee@vmware.com> 19.3-1
- Updated Version
* Mon Dec 12 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19.1-1
- Initial.
