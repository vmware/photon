Summary:          Multipurpose relay (SOcket CAT)
Name:             socat
Version:          1.7.4.4
Release:          3%{?dist}
URL:              http://www.dest-unreach.org/socat
Group:            Applications/Internet
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: http://www.dest-unreach.org/socat/download/%{name}-%{version}.tar.bz2
%define sha512 %{name}=3eedfbf599ecf1d6fd391d03d710044bc5e18a762395bc4cb151b96fe673d405a6630da3070ecddd5ac558126b56aa65feaa74d528eeb755a04aa0ec61690651

Source1: license.txt
%include %{SOURCE1}

%description
Socat is a command line based utility that establishes two bidirectional byte streams and transfers data between them. Because the streams can be constructed from a large set of different types of data sinks and sources (see address types), and because lots of address options may be applied to the streams, socat can be used for many different purposes.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.a' -delete

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.7.4.4-3
- Release bump for SRP compliance
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.7.4.4-2
- Bump version as a part of readline upgrade
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.4.4-1
- Automatic Version Bump
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.4.3-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.0.b9-3
- Bump up release for openssl
* Fri Jul 24 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.0.b9-2
- Add no depreciated option
* Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> 2.0.0.b9-1
- Upgrade to 2.0.0-b9
* Tue Sep 19 2017 Bo Gan <ganb@vmware.com> 1.7.3.2-4
- Disable test 302
* Tue Sep 12 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.3.2-3
- Fix make check issue.
* Tue May 02 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.3.2-2
- Correct the GPL license version.
* Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.3.2-1
- Update to version 1.7.3.2
* Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  1.7.3.1-1
- Initial build.
