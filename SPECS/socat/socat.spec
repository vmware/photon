Summary:          Multipurpose relay (SOcket CAT)
Name:             socat
Version:          2.0.0.b9
Release:          1%{?dist}
License:          GPL2
URL:              http://www.dest-unreach.org/socat
Group:            Applications/Internet
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          http://www.dest-unreach.org/socat/download/%{name}-%{version}.tar.bz2
%define sha1      socat=370edc142ebed68f15581340758fd85757f7b1e9

%description
Socat is a command line based utility that establishes two bidirectional byte streams and transfers data between them. Because the streams can be constructed from a large set of different types of data sinks and sources (see address types), and because lots of address options may be applied to the streams, socat can be used for many different purposes.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}

make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
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
