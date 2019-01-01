%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name rbvmomi

Summary:        Ruby interface to the VMware vSphere API.
Name:           rubygem-rbvmomi
Version:        1.10.0
Release:        3%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/rbvmomi
Source0:        http://rubygems.org/gems/rbvmomi-%{version}.gem
%define sha1    rbvmomi=ad3ec07dfda00cc41e62ba6edb0e205b8a732cb2
BuildRequires:  ruby
Requires:       ruby

%description
RbVmomi is a Ruby interface to the vSphere API. Like the Perl and Java SDKs, you can use it to manage ESX and VirtualCenter servers. The current release supports the vSphere 5.0 API. RbVmomi specific documentation is online and is meant to be used alongside the official documentation.

%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/rbvmomi-%{version}
gem install yard jeweler rake
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.10.0-3
-   Increment the release version as part of ruby upgrade
*   Fri Jun 23 2017 Chang Lee <changlee@vmware.com> 1.10.0-2
-   Updated %check
*   Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-1
-   Updated to version 1.10.0.
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.8.2-4
-   Bump up release number to reflect ruby upgrade
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.8.2-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.2-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.8.2-1
-   Upgrade to 1.8.2
*   Wed Nov 11 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-1
-   Initial build
