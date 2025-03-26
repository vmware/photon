%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name builder

Summary:        Builders for MarkUp
Name:           rubygem-builder
Version:        3.2.4
Release:        4%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://onestepback.org
Source0: http://rubygems.org/gems/builder-%{version}.gem

# Taken from https://github.com/rvm/rvm/blob/master/binscripts/rvm-installer
Source1: rvm-installer

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  ruby

Requires: ruby

%description
Builder provides a number of builder objects that make creating structured
data simple to do. Currently the following builder objects are supported:

%prep
%autosetup -p1 -n %{gem_name}-%{version}
chmod +x %{SOURCE1}
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
*   Wed Jan 22 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.2.4-4
-   Remove shasum for local file rvm-installer
*   Fri Jan 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.2.4-3
-   Bring rvm-installer to spec dir
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.2.4-2
-   Release bump for SRP compliance
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
