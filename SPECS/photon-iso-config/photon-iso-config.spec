%global debug_package %{nil}

Summary:       Photon iso config
Name:          photon-iso-config
Version:       4.0
Release:       1%{?dist}
License:       Apache 2.0 and GPL 2.0
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/vmware/photon/tree/4.0/support/image-builder/iso/BUILD_DVD/isolinux
Source0:       %{name}-%{version}.tar.gz
%define sha512 %{name}=13fb8beb4be8912f53b8190b8faa4b1568eb514dfec717bfc6f8a8fb10810bac32b89ea06e410405dd48405b19cf15bb075bcbcf7ca941f81aa897858fb8512a

%description
Boot menu cfg files and splash screen image to create Photon iso images.

%prep
%autosetup -p1

%build

%install
install -dm0755 %{buildroot}%{_datadir}/%{name}
install -p -m 755 * %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%changelog
* Fri Dec 09 2022 Piyush Gupta <gpiyush@vmware.com> 4.0-1
- Initial build for Photon OS.
