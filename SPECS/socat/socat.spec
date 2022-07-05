Summary:          Multipurpose relay (SOcket CAT)
Name:             socat
Version:          1.7.4.3
Release:          1%{?dist}
License:          GPL2
URL:              http://www.dest-unreach.org/socat
Group:            Applications/Internet
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          http://www.dest-unreach.org/socat/download/%{name}-%{version}.tar.bz2
%define sha512    socat=50c13924b76461feac8d8dab416e23566f834a52ab882ed3b691245c1a635caf2d8185d30a84efef1fb82d8f1edf5a463a9cb31b3d4ce6dc45521f86c29d2dcb

%description
Socat is a command line based utility that establishes two bidirectional byte streams and transfers data between them. Because the streams can be constructed from a large set of different types of data sinks and sources (see address types), and because lots of address options may be applied to the streams, socat can be used for many different purposes.

%prep
%autosetup

%build
%configure

make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
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
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.7.4.3-1
-   Automatic Version Bump
*   Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.0.b9-3
-   Bump up release for openssl
*   Fri Jul 24 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.0.b9-2
-   Add no depreciated option
*   Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> 2.0.0.b9-1
-   Upgrade to 2.0.0-b9
*   Tue Sep 19 2017 Bo Gan <ganb@vmware.com> 1.7.3.2-4
-   Disable test 302
*   Tue Sep 12 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.3.2-3
-   Fix make check issue.
*   Tue May 02 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.3.2-2
-   Correct the GPL license version.
*   Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.7.3.2-1
-   Update to version 1.7.3.2
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  1.7.3.1-1
-   Initial build.
