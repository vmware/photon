%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name rbvmomi

Summary: Ruby interface to the VMware vSphere API.
Name: rubygem-rbvmomi
Version: 1.8.2
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/vmware/rbvmomi
Source0: http://rubygems.org/gems/rbvmomi-%{version}.gem
%define sha1 rbvmomi=565ad4c8433fa38154a00ad661c7e36ad060f9d0
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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.2-2
-	GA - Bump release of all rpms
* 	Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.8.2-1
- 	Upgrade to 1.8.2
* 	Wed Nov 11 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-1
- 	Initial build
