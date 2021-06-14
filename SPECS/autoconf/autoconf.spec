Summary:        The package automatically configure source code
Name:           autoconf
Version:        2.71
Release:        1%{?dist}
License:        GPLv2
URL:            http://www.gnu.org/software/autoconf
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        http://ftp.gnu.org/gnu/autoconf/%{name}-%{version}.tar.xz
%define sha1    autoconf=1b5b1dbed849c6653be47c56d28d26fcf3f7238a
Requires:       perl
BuildRequires:  m4
Requires:       m4
BuildArch:      noarch

%description
The package contains programs for producing shell scripts that can
automatically configure source code.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%check
make -k check %{?_smp_mflags} TESTSUITEFLAGS="1-500"

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%{_datarootdir}/autoconf/*

%changelog
*   Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2.71-1
-   Automatic Version Bump
*   Sun Nov 15 2020 Prashant Singh Chauhan <psinghchauha@vmware.com> 2.69-9
-   Fix for make check failure port test to bash 5.0
*   Wed Sep 11 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 2.69-8
-   Fix for make check failure
*   Wed Oct 17 2018 Dweep Advani <dadvani@vmware.com> 2.69-7
-   Build section is changed to used %configure
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.69-6
-   Fix arch
*   Tue Dec 6 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.69-5
-   Fixed Bug 1718089 make check failure
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.69-4
-   GA - Bump release of all rpms
*   Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 2.69-3
-   Adding m4 package to build and run time required package
*   Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.69-2
-   Adding perl packages to required packages
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.69-1
-   Initial build.	First version
