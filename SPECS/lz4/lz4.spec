Summary:        Extremely fast compression.
Name:           lz4
Version:        1.9.4
Release:        3%{?dist}
URL:            http://lz4.github.io/lz4
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/lz4/lz4/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=043a9acb2417624019d73db140d83b80f1d7c43a6fd5be839193d68df8fd0b3f610d7ed4d628c2a9184f7cde9a0fd1ba9d075d8251298e3eb4b3a77f52736684

Source1: license.txt
%include %{SOURCE1}

%description
LZ4 is lossless compression algorithm, providing compression speed
at 400 MB/s per core, scalable with multi-cores CPU.

It features an extremely fast decoder, with speed in multiple GB/s
per core, typically reaching RAM speed limits on multi-core systems.

%package devel
Summary:    Libraries and header files for lz4
Requires:   %{name} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for lz4.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX="%{_usr}" %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblz4.so.*
%{_datadir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/liblz4.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.9.4-3
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.9.4-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.9.4-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.9.3-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.2-1
- Automatic Version Bump
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.8.2-1
- Update to version 1.8.2
* Wed Mar 29 2017 Michelle Wang <michellew@vmware.com> 1.7.5-1
- Update lz4 package to 1.7.5.
* Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
- Add lz4 package.
