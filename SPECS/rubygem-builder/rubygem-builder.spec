%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name builder

Summary:        Builders for MarkUp
Name:           rubygem-builder
Version:        3.2.3
Release:        2%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://onestepback.org
Source0:        http://rubygems.org/gems/builder-%{version}.gem
%define sha1    builder=5cd6a92e6360279ec1e5c2456372f1709df9a6b2
BuildRequires:  ruby
Requires:       ruby

%description
Builder provides a number of builder objects that make creating structured
data simple to do. Currently the following builder objects are supported:

%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Jan 29 2019 Srinidhi Rao <srinidhir@vmware.com> 3.2.3-2
-   Increment the release version as part of ruby upgrade.
*   Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.3-1
-   Updated to version 3.2.3.
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 3.2.2-3
-   Bump up release number to reflect ruby upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.2-2
-   GA - Bump release of all rpms
*   Wed Nov 11 2015 Xiaolin Li <amakhalov@vmware.com> 3.2.2-1
-   Initial build
