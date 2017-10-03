Summary:       confd is a lightweight configuration management tool
Name:          calico-confd
Version:       0.12.0
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       MIT
URL:           https://github.com/kelseyhightower/confd/releases
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: glide
BuildRequires: go >= 1.7
%define sha1 calico-confd=61b15d926ebb87b466b7355d31e542109f0fad2a

%description
confd is a lightweight configuration management tool that keeps local configuration files up-to-date, and reloading applications to pick up new config file changes.

%prep
%setup -q -n confd-%{version}

%build
export GOPATH="$(pwd)"
cd ..
mv "${GOPATH}" confd
mkdir -p "${GOPATH}/src/github.com/kelseyhightower"
mv confd "${GOPATH}/src/github.com/kelseyhightower/"

cd "${GOPATH}/src/github.com/kelseyhightower/confd"
./build

%install
pushd src/github.com/kelseyhightower/confd
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ bin/confd

%files
%defattr(-,root,root)
%{_bindir}/confd

%changelog
*    Thu Oct 12 2017 Bo Gan <ganb@vmware.com> 0.12.0-2
-    fix GOPATH
*    Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.0-1
-    Calico confd for PhotonOS.
