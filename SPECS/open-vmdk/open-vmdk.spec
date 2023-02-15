Summary:       Tools to create OVA files from raw disk images
Name:          open-vmdk
Version:       0.1.0
Release:       1%{?dist}
Vendor:        VMware, Inc.
Distribution:  Photon
License:       Apache License 2.0
URL:           https://github.com/vmware/open-vmdk
Group:         Development/Tools

Source0:       https://github.com/vmware/open-vmdk/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=3490e389a7e49b7cde9c1e1a4d97ad7d6873b2db55f1da4b54b2a5fb98d0f9bba43121fd5ed53afa81e768fa8c330f2ba1ff5780855692a0fb416b7db13467f9

BuildRequires: zlib-devel

Requires: coreutils
Requires: zlib
Requires: tar
Requires: grep
Requires: sed

%description
Tools to create OVA files from raw disk images. This includes 'vmdk-convert'
to create VMDKs from raw disk images, and 'mkova.sh' to create OVA files
that can be imported by VMware vSphere or Fusion and Workstation.

%prep
%autosetup

%build
%make_build

%install
%make_install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install ova/*.ovf %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{name}/*

%changelog
* Wed Feb 15 2023 Oliver Kurth <okurth@vmware.com> 0.1.0-1
- initial release