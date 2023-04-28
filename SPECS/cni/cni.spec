Summary:        Container Network Interface (CNI) plugins
Name:           cni
Version:        1.1.1
Release:        3%{?dist}
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

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_default_cni_plugins_dir}/*

%changelog
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.1.1-3
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.1-2
- Bump up version to compile with new go
* Sat Nov 19 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.1-1
- Upgrade to v1.1.1
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-14
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-11
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-10
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-9
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.8.7-8
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.7-7
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.7-6
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 0.8.7-5
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 0.8.7-4
- Bump up version to compile with new go
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
