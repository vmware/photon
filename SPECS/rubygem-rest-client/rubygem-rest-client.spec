%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rest-client

Name:           rubygem-rest-client
Version:        2.1.0
Release:        7%{?dist}
Summary:        A simple HTTP and REST client for Ruby, inspired by the Sinatra microframework style of specifying actions: get, put, post, delete.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=fe5d44409dfe607566b4c0324441d9a3981776699027bfbc92283b1cd425f204211fc872593cb0784e0ca7a5e061e98793540eedfeb1891d9a8afd53a5ce01de

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-http-cookie
BuildRequires: rubygem-mime-types
BuildRequires: rubygem-http-accept < 2.0
BuildRequires: rubygem-netrc

Requires: rubygem-http-cookie >= 1.0.2, rubygem-http-cookie < 2.0.0
Requires: rubygem-mime-types >= 1.16.0, rubygem-mime-types < 4.0.0
Requires: rubygem-netrc >= 0.8.0, rubygem-netrc < 1.0.0
Requires: rubygem-http-accept < 2.0
Requires: ruby

%description
A simple HTTP and REST client for Ruby, inspired by the Sinatra microframework style of specifying actions: get, put, post, delete.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
mkdir -p %{buildroot}%{_bindir}
%gem_install
ln -srv %{buildroot}%{gemdir}/bin/restclient %{buildroot}%{_bindir}/restclient

%files
%defattr(-,root,root,-)
%{gemdir}
%{_bindir}/restclient

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1.0-7
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.1.0-6
- Bump Version to build with new ruby
* Mon Dec 18 2023 Shivani Agarwal <shivania2@vmware.com> 2.1.0-5
- Add restclient symlink
* Mon Oct 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.1.0-4
- Fix requires
* Tue Nov 29 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.0-3
- Version bump to build with rubygem-http-accept-2.2.0
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 2.1.0-2
- rebuilt with ruby-2.7.1
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.1.0-1
- Initial build
