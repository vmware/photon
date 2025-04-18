%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name optimist

Summary:        Optimist is a commandline option parser for Ruby that just gets out of your way.
Name:           rubygem-optimist
Version:        3.1.0
Release:        3%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/%{gem_name}

Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=adadc1722d970cc4c002a0983d0ab2dbb3683777310c7085950e07fa18c94e4ab788bd10bca9e1d076cf77637d09e2d6bb969f5d5b35f0b648881e744f42c785

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Optimist is a commandline option parser for Ruby that just gets out of your way.
One line of code per option is all you need to write.
For that, you get a nice automatically-generated help page, robust option parsing,
and sensible defaults for everything you don't specify.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.0-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.0-2
- Bump Version to build with new ruby
* Mon Oct 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.1.0-1
- Intial version, needed by rubygems-rbvmomi
