Summary: Network traffic statics utility for Solaris and Linux
Name:    nicstat
Version: 1.95
Release: 3%{?dist}
License:	Artistic License 2.0
URL:		http://sourceforge.net/projects/%{name}
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%define sha1 nicstat=e6cfe836e674de9acd73bfd1ec82d28092ccf7cd
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

%description
Nicstat is a Solaris and Linux command-line that prints out network statistics for all network interface cards (NICs), including packets, kilobytes per second, average packet sizes and more.

%prep
%setup -q

%build
gcc  -o3 $([ $(uname -m) = x86_64 ] && echo -m64) %{name}.c -o %{name}

%install
install -p -m755 -D  %{name} %{buildroot}%{_bindir}/%{name}
install -p -m644 -D  %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%files
%{_bindir}/*
%{_mandir}/man1/*

%changelog
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.95-3
-   Aarch64 support
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.95-2
-	GA - Bump release of all rpms
*	Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 1.95-1
-       Initial build.  First version
