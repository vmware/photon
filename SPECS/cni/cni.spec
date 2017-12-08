Summary:        Container Network Interface (CNI) plugins
Name:           cni
Version:        0.6.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/containernetworking/cni
Source0:        https://github.com/containernetworking/cni/archive/%{name}-v%{version}.tar.gz
%define sha1 cni=f273e53c6d019d5cc9dfb75b48e619aa52abcce7
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go >= 1.5
%define _default_cni_plugins_dir /opt/cni/bin

%description
The CNI (Container Network Interface) project consists of a specification and libraries for writing plugins to configure network interfaces in Linux containers, along with a number of supported plugins.

%prep
%setup -n plugins-%{version}

%build
./build.sh

%install
install -vdm 755 %{buildroot}%{_default_cni_plugins_dir}
install -vpm 0755 -t %{buildroot}%{_default_cni_plugins_dir} bin/*

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post

%postun

%files
%defattr(-,root,root)
%{_default_cni_plugins_dir}/*

%changelog
*   Tue Dec 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.6.0-1
-   cni v0.6.0.
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-1
-   Version update
*   Thu Feb 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.0-1
-   Add CNI plugins package to PhotonOS.
