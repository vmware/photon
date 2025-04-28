#need to deactivate debuginfo since debugfiles.list is empty
%define debug_package %{nil}

Summary:        Thin provisioning tools
Name:           thin-provisioning-tools
Version:        1.0.2
Release:        7%{?dist}
Group:          System Environment/Base
URL:            https://github.com/jthornber/thin-provisioning-tools
Source0:        thin-provisioning-tools-%{version}.tar.gz
Source1:        thin-provisioning-tools-deps-%{version}p1.tar.xz

Source2: license.txt
%include %{SOURCE2}
BuildRequires:  expat-devel
BuildRequires:  libaio-devel
BuildRequires:  boost-devel
BuildRequires:  rust
Requires:       expat
Requires:       libaio
Requires:       libgcc
Vendor:         VMware, Inc.
Distribution:   Photon

%description
thin-provisioning-tools contains check,dump, restore, repair, rmap and metadata_size tools to manage device-mapper thin provisioning target metadata devices;
cache check, dump, metadata_size, restore and repair tools to manage device-mapper cache metadata devices are included and era check, dump, restore and invalidate to manage snapshot eras.

%prep
%autosetup
tar -xf %{SOURCE1} -C /root

%build
cargo build --release --offline

%install
%make_install DATADIR=%{buildroot}/%{_datadir} BINDIR=%{buildroot}/%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mandir}/man8/*
%{_bindir}/*

%changelog
* Mon Apr 28 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.0.2-7
- Bump for building with updated libaio
* Wed Apr 09 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.0.2-6
- Version bump for expat upgrade
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0.2-5
- Release bump for SRP compliance
* Thu Aug 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.0.2-4
- Bump up version as part of rust upgrade.
* Thu Mar 23 2023 Srish Srinivasan <ssrish@vmware.com> 1.0.2-3
- Altered build process
* Mon Mar 20 2023 Srish Srinivasan <ssrish@vmware.com> 1.0.2-2
- Fix build error
* Thu Feb 16 2023 Gerrit Photon <photon-checkins@vmware.com> 1.0.2-1
- Automatic Version Bump
* Wed Sep 02 2020 Gerrit Photon <photon-checkins@vmware.com> 0.9.0-1
- Automatic Version Bump
* Wed Jun 10 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.5-1
- Automatic Version Bump
* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 0.7.0-1
- Update version to stable release version 0.7.0.
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.6.3-3
- Use standard configure macros
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.3-2
- Ensure non empty debuginfo
* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 0.6.3-1
- Updated to version 0.6.3.
* Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.6.1-3
- Fix gcc-6.3 compilation errors
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.1-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 0.6.1-1
- Updating version
* Tue Mar 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.4.1-1
- Initial version
