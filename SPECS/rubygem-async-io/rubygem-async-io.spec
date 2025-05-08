Name:           rubygem-async-io
Summary:        Provides support for asynchonous TCP, UDP, UNIX and SSL sockets.
Version:        1.34.0
Release:        6%{?dist}
Group:          Development/Libraries
URL:            https://vmware.github.io/photon
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: license.txt
%include %{SOURCE0}

BuildArch: noarch

# Keep this list alphabetically sorted
Requires: rubygem-io-endpoint
Requires: rubygem-io-stream

%description
Metapackage to install rubygem-async-io

%prep
%build

%files
%defattr(-,root,root,0755)

%changelog
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.34.0-6
- Changing to metapackage for rubygem-async-io
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.34.0-5
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.34.0-4
- Release bump for SRP compliance
* Tue Apr 16 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.34.0-3
- Fix ruby version in buildrequires
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.34.0-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.34.0-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.30.1-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.30.0-1
- Automatic Version Bump
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.25.0-1
- Initial build
