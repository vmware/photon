Summary:        Container Network Interface (CNI) plugins
Name:           cni
Version:        0.5.1
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/containernetworking/cni
Source0:        https://github.com/containernetworking/cni/archive/%{name}-v%{version}.tar.gz
%define sha1 cni=c704cff26d8e786ca0efbd1751bf51fb7f64f1b3
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go >= 1.5
%define _default_cni_plugins_dir /opt/cni/bin

%description
The CNI (Container Network Interface) project consists of a specification and libraries for writing plugins to configure network interfaces in Linux containers, along with a number of supported plugins.

%prep
%setup -n %{name}-%{version}

%build
./build

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
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-1
-   Version update
*   Thu Feb 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.0-1
-   Add CNI plugins package to PhotonOS.
