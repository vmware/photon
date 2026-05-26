%define debug_package %{nil}

Summary:        CoreDNS
Name:           coredns
Version:        1.14.3
Release:        1%{?dist}
License:        Apache License 2.0
URL:            https://github.com/%{name}/%{name}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/coredns/coredns/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=39b87ff29460e8eb2fd9db53ae6fe19d7b7c99da0a7cfc9e93b22d93c2c53c5cfd2bb493610901a6cfae578430d1fc215b9c9d70e95cc31f0c4084b618e60864

BuildRequires: go
BuildRequires: git

%description
CoreDNS is a DNS server that chains plugins

%prep
%autosetup -p1

%build
%make_build

%install
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}

%changelog
* Tue May 26 2026 Dweep Advani <dweep.advani@broadcom.com> 1.14.3-1
- Upgrade to 1.14.3 to fix CVE-2026-32934/2936/3190/3489
* Fri Mar 13 2026 Dweep Advani <dweep.advani@broadcom.com> 1.11.1-11
- Fix CVE-2026-26017 and CVE-2026-26018
* Mon Nov 10 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.11.1-10
- Bump up as part of go upgrade
* Tue Sep 16 2025 Dweep Advani <dweep.advani@broadcom.com> 1.11.1-9
- Fix CVE-2025-58063
* Thu Jun 26 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.11.1-8
- Fix build instructions
* Mon Jun 23 2025 Dweep Advani <dweep.advani@broadcom.com> 1.11.1-7
- Fix for CVE-2025-47950
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.11.1-6
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.11.1-5
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.11.1-4
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.11.1-3
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.11.1-2
- Bump up version to compile with new go
* Fri Nov 03 2023 Nitesh Kumar <kunitesh@vmware.com> 1.11.1-1
- Version upgrade to v1.11.1 to fix following CVE's:
- CVE-2021-28235 and CVE-2023-32082
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.10.1-3
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.10.1-2
- Bump up version to compile with new go
* Tue Jul 04 2023 Nitesh Kumar <kunitesh@vmware.com> 1.10.1-1
- Version upgrade to v1.10.1 to fix following CVE's:
- CVE-2018-1098, CVE-2018-1099, CVE-2023-0296,
- CVE-2020-15106, CVE-2020-15112, CVE-2020-15113,
- CVE-2020-15114, CVE-2020-15115, CVE-2020-15136
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.7.1-19
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.7.1-18
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.7.1-17
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-16
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-11
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-10
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-9
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.7.1-7
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.7.1-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.7.1-5
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.7.1-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.7.1-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.7.1-2
-   Bump up version to compile with new go
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.1-1
-   Automatic Version Bump
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
-   Automatic Version Bump
*   Sun Sep 22 2019 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-3
-   Fix compilation issue (do not compile mholt/caddy).
*   Sun Sep 23 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-2
-   Fix compilation issue.
-   aarch64 support.
*   Fri Aug 03 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.2.0-1
-   Initial version of coredns 1.2.0.
