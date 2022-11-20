Summary:        Kubernetes security benchmarking tool
Name:           kube-bench
Version:        0.6.10
Release:        2%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://github.com/aquasecurity/%{name}
Group:          Development/Tools

Source0: https://github.com/aquasecurity/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=183ae317008a278f148318b72bdffb954a95527db46189bc88147c6847cf787a625dcb00dcd2ad6d3e89ba65f3ce7c8c074c25ba6f08ed29dfc2493935aa522d

BuildRequires:  git
BuildRequires:  go

%description
The Kubernetes Bench for Security is a Go application that checks
whether Kubernetes is deployed according to security best practices.

%prep
%autosetup -p1

%build
export GOPATH=%{_builddir}
export KUBEBENCH_VERSION=%{version}-%{release}
%make_build build

%install
mkdir -p %{buildroot}%{_bindir}
cp %{name} %{buildroot}%{_bindir}

%if 0%{?with_check}
%check
make tests %{?_smp_mflags}
%endif

%files
%defattr(-,root,root,0755)
%{_bindir}/%{name}
%exclude %dir %{_libdir}/debug

%changelog
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 0.6.10-2
- Bump up version to compile with new go
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.6.10-1
- Upgrade to v0.6.10
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-6
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 0.3.1-5
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.1-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.3.1-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.3.1-2
- Bump up version to compile with new go
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.3.1-1
- Automatic Version Bump
* Wed Oct 30 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.34-1
- Initial
