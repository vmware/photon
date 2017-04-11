Summary:        Overlay network for containers based on etcd
Name:           flannel
Version:        0.7.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/coreos/flannel
Source0:        https://github.com/coreos/flannel/archive/%{name}-%{version}.zip
%define sha1 flannel=758fc9c4b3b3631de2b73b1f00898a4c72589b58
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  etcd >= 2.0.0
BuildRequires:  gcc
BuildRequires:  unzip
BuildRequires:  go
BuildRequires:  git
BuildRequires:	systemd
BuildRequires:	vim
Requires:       etcd >= 2.0.0

%description
flannel is a virtual network that provides a subnet to a container runtime
host OS for use with containers. flannel uses etcd to store the network
configuration, allocated subnets, and additional data.

%prep
%setup -n %{name}-%{version}
%build
mkdir -p src/github.com/coreos/flannel
cp -r backend \
      dist \
      network \
      pkg \
      remote \
      subnet \
      vendor \
      version \
      src/github.com/coreos/flannel/
cp -r vendor/github.com/golang src/github.com/
cp -r vendor/golang.org src/
cp -r vendor/github.com/coreos/pkg src/github.com/coreos/
export GOPATH=$(pwd)
make dist/flanneld

%install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ dist/flanneld

%check
export GOPATH=%{_builddir}
go get golang.org/x/tools/cmd/cover
sed -e 's:^func TestRemote:func _TestRemote:' -i remote/remote_test.go || die
./test

%post

%postun

%files
%defattr(-,root,root)
%{_bindir}/flanneld

%changelog
*	Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 0.7.0-1
-	Updated to version 0.7.0
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5.5-2
-	GA - Bump release of all rpms
*   	 Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.5.5-1
-   	 Upgraded to version 0.5.5
*        Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.5.2-1
-        Add flannel package to photon.
