Summary:        Container Network Interface (CNI) plugins
Name:           cni
Version:        1.1.1
Release:        8%{?dist}
License:        ASL 2.0
URL:            https://github.com/containernetworking/plugins
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containernetworking/plugins/archive/%{name}-v%{version}.tar.gz
%define sha512 %{name}=03da31caee5f9595abf65d4a551984b995bc18c5e97409549f08997c5a6a2b41a8950144f8a5b4f810cb401ddbe312232d2be76ec977acf8108eb490786b1817

BuildRequires:  go

%define _default_cni_plugins_dir /opt/cni/bin

%description
The CNI (Container Network Interface) project consists of a specification and
libraries for writing plugins to configure network interfaces in Linux containers,
along with a number of supported plugins.

%prep
%autosetup -p1 -n plugins-%{version}

%build
sh ./build_linux.sh

%install
install -vdm 755 %{buildroot}%{_default_cni_plugins_dir}
install -vpm 0755 -t %{buildroot}%{_default_cni_plugins_dir} bin/*

%if 0%{?with_check}
%check
make -k check %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_default_cni_plugins_dir}/*

%changelog
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-8
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-7
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-6
- Bump up version to compile with new go
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-5
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-3
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-2
- Bump up version to compile with new go
* Thu Nov 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.1-1
- Upgrade v1.1.1
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.9.1-5
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.9.1-4
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 0.9.1-3
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.9.1-2
- Bump up version to compile with new go
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 0.9.1-1
- Automatic Version Bump
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.8.7-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.8.7-2
- Bump up version to compile with new go
* Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.7-1
- Automatic Version Bump
* Mon Jul 13 2020 Susant Sahani <ssahani@vmware.com> 0.8.6-1
- Bump up version
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.8.3-2
- Bump up version to compile with go 1.13.3-2
* Fri Dec 6 2019 Ashwin H <ashwinh@vmware.com> 0.8.3-1
- Update cni to v0.8.3
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 0.7.5-3
- Bump up version to compile with go 1.13.3
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.7.5-2
- Bump up version to compile with new go
* Tue Apr 02 2019 Ashwin H <ashwinh@vmware.com> 0.7.5-1
- Update cni to v0.7.5
* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-1
- Version update
* Thu Feb 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.0-1
- Add CNI plugins package to PhotonOS.
