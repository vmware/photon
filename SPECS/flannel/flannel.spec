Summary:        Overlay network for containers based on etcd
Name:           flannel
Version:        0.7.1
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://github.com/coreos/flannel
Source0:        https://github.com/coreos/flannel/archive/%{name}-%{version}.tar.gz
%define sha1 flannel=3626430734a705f3a907f05f0c9a0ac33f5397dc
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  etcd >= 2.0.0
BuildRequires:  gcc
BuildRequires:  unzip
BuildRequires:  go
Requires:       etcd >= 2.0.0

%description
flannel is a virtual network that provides a subnet to a container runtime
host OS for use with containers. flannel uses etcd to store the network
configuration, allocated subnets, and additional data.

%prep
%setup -cqn src/github.com/coreos/

%build
export GOPATH=%{_builddir}
echo $GOAPTH
mv %{name}-%{version}  %{name}
pushd %{name}
make dist/flanneld
popd

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ %{name}/dist/flanneld

%check
cd %{name}
GOPATH=%{_builddir} make test

%post

%postun

%files
%defattr(-,root,root)
%{_bindir}/flanneld

%changelog
*	Tue Aug 29 2017 Chang Lee <changlee@vmware.com> 0.7.1-2
-	Fixed %check according to version upgrade
*	Fri May 05 2017 Chang Lee <changlee@vmware.com> 0.7.1-1
-	Updated to version 0.7.1
*	Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 0.7.0-1
-	Updated to version 0.7.0
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5.5-2
-	GA - Bump release of all rpms
*   	 Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.5.5-1
-   	 Upgraded to version 0.5.5
*        Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.2-1
-        Add flannel package to photon.
