%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name rbvmomi

Summary: Ruby interface to the VMware vSphere API.
Name: rubygem-rbvmomi
Version: 1.8.1
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/vmware/rbvmomi
Source0: http://rubygems.org/gems/rbvmomi-%{version}.gem
%define sha1 rbvmomi=ab4cfcc08f33a68ba2e10f67e0f8521e0b8988c2
BuildRequires: ruby
Requires: ruby

%description
RbVmomi is a Ruby interface to the vSphere API. Like the Perl and Java SDKs, you can use it to manage ESX and VirtualCenter servers. The current release supports the vSphere 5.0 API. RbVmomi specific documentation is online and is meant to be used alongside the official documentation.

%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Nov 11 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-1
- Initial build
