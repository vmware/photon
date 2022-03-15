Summary:        Container Network Interface (CNI) plugins
Name:           cni
Version:        0.8.7
Release:        10%{?dist}
License:        ASL 2.0
URL:            https://github.com/containernetworking/plugins
Source0:        https://github.com/containernetworking/plugins/archive/%{name}-v%{version}.tar.gz
%define sha512  cni=1b11b080b1f54a8a792b1048573d7d882603b76929f0c9343eeb2e010f97700c0deea4489faeb493a1aeac12557b6847b26784c378d0430c47de6bdaca6aa70f
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
%define _default_cni_plugins_dir /opt/cni/bin

%description
The CNI (Container Network Interface) project consists of a specification and
libraries for writing plugins to configure network interfaces in Linux containers,
along with a number of supported plugins.

%prep
%autosetup -n plugins-%{version}

%build
./build_linux.sh

%install
install -vdm 755 %{buildroot}%{_default_cni_plugins_dir}
install -vpm 0755 -t %{buildroot}%{_default_cni_plugins_dir} bin/*

%check
make -k check %{?_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_default_cni_plugins_dir}/*

%changelog
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-10
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-9
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.7-7
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.7-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.7-5
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.8.7-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.8.7-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.8.7-2
-   Bump up version to compile with new go
*   Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.7-1
-   Automatic Version Bump
*   Mon Jul 13 2020 Susant Sahani <ssahani@vmware.com> 0.8.6-1
-   Bump up version
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.8.3-2
-   Bump up version to compile with go 1.13.3-2
*   Fri Dec 6 2019 Ashwin H <ashwinh@vmware.com> 0.8.3-1
-   Update cni to v0.8.3
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 0.7.5-3
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.7.5-2
-   Bump up version to compile with new go
*   Tue Apr 02 2019 Ashwin H <ashwinh@vmware.com> 0.7.5-1
-   Update cni to v0.7.5
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-1
-   Version update
*   Thu Feb 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.0-1
-   Add CNI plugins package to PhotonOS.
