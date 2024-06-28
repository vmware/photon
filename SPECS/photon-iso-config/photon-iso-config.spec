%global debug_package %{nil}

Summary:       Photon iso config
Name:          photon-iso-config
Version:       5.0
Release:       2%{?dist}
License:       Apache 2.0 and GPL 2.0
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/vmware/photon/tree/4.0/support/image-builder/iso/BUILD_DVD/isolinux
Source0:       %{name}-%{version}.tar.gz
%define sha512 %{name}=e199a1bda8b715a96107dd8ed8ca4ac0372d2b8dadbec19b7d97e96747b20bf0c3c96ba59eb637a6b3001123a528cbdb84ebae351e9da7402fe7e8eef96fb1f3
Source1:       splash.png

%description
Boot menu cfg files and splash screen image to create Photon iso images.

%prep
%autosetup -p1

%build

%install
install -dm0755 %{buildroot}%{_datadir}/%{name}
install -p -m 755 * %{buildroot}%{_datadir}/%{name}
cp -p %{SOURCE1} %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%changelog
* Thu Mar 23 2023 Piyush Gupta <gpiyush@vmware.com> 5.0-2
- Update splash screen.
* Fri Dec 09 2022 Piyush Gupta <gpiyush@vmware.com> 5.0-1
- Initial build for Photon OS.
