%global debug_package %{nil}
%global gem_name unf_ext

Name: rubygem-unf_ext
Version:        0.0.9.1
Release:        3%{?dist}
Summary:        Unicode Normalization Form support library for CRuby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=f2d0d58dc0ed30e3e99ac75022c8ea78bf4ad51c8803009c059de087b1cd439e06a8e7ef4c1be5c75048f85afe6c301f402ed21405ff02ad36ea73209416994d

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel
BuildRequires:  gmp-devel

Requires:       ruby

%description
Unicode Normalization Form support library for CRuby.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.0.9.1-3
- Build gems properly
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.9.1-2
- Add gem macros
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.0.9.1-1
- Update to version 0.0.9.1
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.0.8.2-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.0.7.7-1
- Automatic Version Bump
* Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-2
- Enabled build for non x86_64 build archs
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.0.7.6-1
- Initial build
