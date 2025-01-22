%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name builder

Summary:        Builders for MarkUp
Name:           rubygem-builder
Version:        3.2.4
Release:        2%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://onestepback.org

Source0:        http://rubygems.org/gems/builder-%{version}.gem
%define sha512  builder=730317ec0a4af33e183283e309e38d47deb08db0ab6bd6dfebdedcebb7470bd383c6c1d32ad674adc43298e0f86930b97c652fff9827ca8890db2d1d68e792f1

# Taken from https://github.com/rvm/rvm/blob/master/binscripts/rvm-installer
Source1:        rvm-installer

BuildRequires:  ruby

Requires: ruby

%description
Builder provides a number of builder objects that make creating structured
data simple to do. Currently the following builder objects are supported:

%prep
%autosetup -p1 -c -T
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
*   Mon Jan 20 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.2.4-2
-   Bring rvm-installer to spec dir
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.4-1
-   Automatic Version Bump
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
