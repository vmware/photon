Summary:        Container Network Interface (CNI) plugins
Name:           cni
Version:        1.1.1
Release:        9%{?dist}
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
eu-elfcompress -q -p -t none %{buildroot}%{_default_cni_plugins_dir}/*

%if 0%{?with_check}
%check
make -k check %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_default_cni_plugins_dir}/*

%changelog
* Mon Jun 24 2024 Mukul Sikka <msikka@vmware.com> 1.1.1-9
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-8
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-7
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-6
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-5
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-3
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-2
- Bump up version to compile with new go
* Mon Jan 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.1-1
- Upgrade to v1.1.1
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-17
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-16
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-15
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-14
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-13
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-12
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-11
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-10
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.6-9
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.6-8
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.6-7
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 0.8.6-6
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.6-5
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 0.8.6-4
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 0.8.6-3
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 0.8.6-2
- Bump up version to compile with new go
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
