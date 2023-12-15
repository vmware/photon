%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name optimist

Summary:        Optimist is a commandline option parser for Ruby that just gets out of your way.
Name:           rubygem-optimist
Version:        3.1.0
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/%{gem_name}

Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=adadc1722d970cc4c002a0983d0ab2dbb3683777310c7085950e07fa18c94e4ab788bd10bca9e1d076cf77637d09e2d6bb969f5d5b35f0b648881e744f42c785

BuildRequires: ruby

Requires: ruby

%description
Optimist is a commandline option parser for Ruby that just gets out of your way.
One line of code per option is all you need to write.
For that, you get a nice automatically-generated help page, robust option parsing,
and sensible defaults for everything you don't specify.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 3.1.0-1
- Intial version, needed by rubygems-rbvmomi
