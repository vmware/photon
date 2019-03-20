Summary:          Multipurpose relay (SOcket CAT)
Name:             socat
Version:          1.7.3.1
Release:          1%{?dist}
License:          GPL
URL:              http://www.dest-unreach.org/socat
Group:            Applications/Internet
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          http://www.dest-unreach.org/socat/download/%{name}-%{version}.tar.bz2
%define sha1      socat=2a5a6013dff9b4954303c6fd5680a86cfd66aa64
Patch0:           openssl-1.1.patch
BuildRequires:    openssl-devel
Requires:         openssl

%description
Socat is a command line based utility that establishes two bidirectional byte streams and transfers data between them. Because the streams can be constructed from a large set of different types of data sinks and sources (see address types), and because lots of address options may be applied to the streams, socat can be used for many different purposes.

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
#*   Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 2.0.0.b9-1
#-   Updating to 2.0.0.b9 release
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  1.7.3.1-1
-   Initial build.
