%global debug_package %{nil}

Summary:       Photon iso config
Name:          photon-iso-config
Version:       5.0
Release:       3%{?dist}
Group:         System Environment/Base
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/vmware/photon/tree/4.0/support/image-builder/iso/BUILD_DVD/isolinux
Source0:       %{name}-%{version}.tar.gz
Source1:       splash.png

Source2: license.txt
%include %{SOURCE2}

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-3
- Release bump for SRP compliance
* Thu Mar 23 2023 Piyush Gupta <gpiyush@vmware.com> 5.0-2
- Update splash screen.
* Fri Dec 09 2022 Piyush Gupta <gpiyush@vmware.com> 5.0-1
- Initial build for Photon OS.
