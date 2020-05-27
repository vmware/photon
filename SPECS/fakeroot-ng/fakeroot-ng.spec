Summary:      Fools programs into thinking they are running with root permission
Name:         fakeroot-ng
Version:      0.18
Release:      3%{?dist}
License:      GPLv2+
URL:          http://fakeroot-ng.lingnu.com/
Source0:      http://downloads.sourceforge.net/project/fakerootng/fakeroot-ng/%{version}/fakeroot-ng-%{version}.tar.gz
%define sha1 fakeroot-ng=288dadbd50ff36a9eb11d4bc14213c6d1beaafaa
Group:        System Environment/Base
BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Group:        Development/Tools
Vendor:       VMware, Inc.
Distribution: Photon
BuildArch:    x86_64

%description
Fakeroot-ng is a clean re-implementation of fakeroot. The core idea 
is to run a program, but wrap all system calls that program performs 
so that it thinks it is running as root, while it is, in practice, 
running as an unprivileged user. When the program is trying to perform 
a privileged operation (such as modifying a file's owner or creating 
a block device), this operation is emulated, so that an unprivileged 
operation is actually carried out, but the result of the privileged 
operation is reported to the program whenever it attempts to query 
the result. 

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{_bindir}/fakeroot-ng
%doc %{_mandir}/man1/fakeroot-ng.1.gz

%changelog
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 0.18-3
-   Adding BuildArch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.18-2
-   GA - Bump release of all rpms
*   Fri Jul 10 2015 Luis Zuniga <lzuniga@vmware.com> 0.17-0.1
-   Initial build for Photon

