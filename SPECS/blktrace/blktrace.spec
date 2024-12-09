Summary:        Utilities for block layer IO tracing
Name:           blktrace
Version:        1.3.0
Release:        2%{?dist}
URL:            http://git.kernel.org/cgit/linux/kernel/git/axboe/blktrace.git/tree/README
Group:          Development/Tools/Other
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/axboe/blktrace.git/snapshot/%{name}-%{version}.tar.gz
%define sha512  blktrace=ad2bff481c1a2f972c1319f463bfea16fc3cb7d76173ebc2fe38c2c39a6b28c8f6492d65580ad2aa38f8a701f5439aa30c11336eebf62bbfc51c9a71b67748d9

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  libaio-devel
Requires:       libaio

%description
blktrace is a block layer IO tracing mechanism which provides detailed information about request queue operations up to user space.

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir} %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%doc README
%defattr(-,root,root)
%{_bindir}
%{_mandir}

%changelog
*   Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.3.0-2
-   Release bump for SRP compliance
*   Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.0-1
-   Automatic Version Bump
*   Thu Jan 24 2019 Tapas Kundu <tkundu@vmware.com> 1.2.0-3
-   Fix for CVE-2018-10689.
*   Sun Sep 23 2018 Sujay G <gsujay@vmware.com> 1.2.0-2
-   Bump blktrace version to 1.2.0
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.0-1
-   Updated to version 1.1.0
*   Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.5-1
-   Initial build.First version
