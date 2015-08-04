%global commit	ed470048eed1c50ca042d3fbc7ac4e5d86bd64d5

Summary:        Overlay network for containers based on etcd
Name:           flannel
Version:        0.5.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/coreos/flannel
Source0:        https://github.com/coreos/flannel/archive/%{commit}/flannel-ed47004.tar.gz
%define sha1 flannel-ed47004=c71c695e51fc9adb81f0e94f13451a4fbf12fd16
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  etcd >= 2.0.0
BuildRequires:  gcc
BuildRequires:  go
Requires:       etcd >= 2.0.0

%description
flannel is a virtual network that provides a subnet to a container runtime
host OS for use with containers. flannel uses etcd to store the network
configuration, allocated subnets, and additional data.

%prep
%setup -n %{name}-%{commit}

%build
./build

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ bin/flanneld

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post

%postun

%files
%defattr(-,root,root)
%{_bindir}/flanneld

%changelog
*        Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.2-1
-        Add flannel package to photon.
