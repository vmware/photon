%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name builder

Summary:        Builders for MarkUp
Name:           rubygem-builder
Version:        3.2.3
Release:        3%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://onestepback.org
Source0:        http://rubygems.org/gems/builder-%{version}.gem
%define sha1    builder=5cd6a92e6360279ec1e5c2456372f1709df9a6b2
Source1:        https://get.rvm.io/rvm-installer
%define sha1    rvm-installer=cf0184a1fc3c0854da5acc1134fac150461d7360
BuildRequires:  ruby
Requires: ruby

%description
Builder provides a number of builder objects that make creating structured
data simple to do. Currently the following builder objects are supported:

%prep
%setup -q -c -T
chmod +x  %{SOURCE1}
cp %{SOURCE1} .
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
./rvm-installer
export PATH=$PATH:/usr/local/rvm/bin
pushd  %{buildroot}%{gemdir}/gems/builder-%{version}/
rake test
popd

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 3.2.3-3
-   Increment the release version as part of ruby upgrade
*   Wed Mar 22 2017 Chang Lee <changlee@vmware.com> 3.2.3-2
-   Updated %check to dynamic gem version
*   Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.3-1
-   Updated to version 3.2.3.
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 3.2.2-4
-   Bump up release number to reflect ruby upgrade
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.2.2-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.2-2
-   GA - Bump release of all rpms
*   Wed Nov 11 2015 Xiaolin Li <amakhalov@vmware.com> 3.2.2-1
-   Initial build
