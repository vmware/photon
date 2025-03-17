Summary: Network traffic statics utility for Solaris and Linux
Name:    nicstat
Version: 1.95
Release: 4%{?dist}
URL:            http://sourceforge.net/projects/%{name}
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

Source1: license.txt
%include %{SOURCE1}

%description
Nicstat is a Solaris and Linux command-line that prints out network statistics for all network interface cards (NICs), including packets, kilobytes per second, average packet sizes and more.

%prep
%autosetup -p1

%build
gcc  -o3 $([ $(uname -m) = x86_64 ] && echo -m64) %{name}.c -o %{name}

%install
install -p -m755 -D  %{name} %{buildroot}%{_bindir}/%{name}
install -p -m644 -D  %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%files
%{_bindir}/*
%{_mandir}/man1/*

%changelog
*   Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.95-4
-   Release bump for SRP compliance
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.95-3
-   Aarch64 support
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.95-2
-   GA - Bump release of all rpms
*   Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 1.95-1
-   Initial build.  First version
