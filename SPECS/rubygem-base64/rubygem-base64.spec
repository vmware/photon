%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name base64

Name:           rubygem-base64
Version:        0.1.1
Release:        1%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=b7b674a88d08d763441050e51c274306fafa6961917eec95e5caeb9406ac3364c6d718bee2df6bbc49cdd1f0b14288a4dbe7773195df9f81750b7815277e59b5

BuildRequires:  ruby

BuildArch: noarch

%description
Provides low level cross-platform primitives for constructing
event loops, with support for select, kqueue, epoll and io_uring.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 0.1.1-1
- Initial version. Needed by rubygem-activesupport.
