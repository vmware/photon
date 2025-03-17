%global debug_package %{nil}
%global gem_name yajl-ruby

Name:           rubygem-yajl-ruby
Version:        1.4.3
Release:        4%{?dist}
Summary:        Ruby C bindings to the excellent Yajl JSON stream-based parser library.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/yajl-ruby-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires:       ruby

%description
Ruby C bindings to the excellent Yajl JSON stream-based parser library.

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
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.3-4
- Release bump for SRP compliance
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.3-3
- Add gem macros
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.3-2
- Build from source
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.4.3-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.4.1-2
- Rebuilt using ruby-2.7.1
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.4.1-1
- Update to version 1.4.1
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
- Initial build
