%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name retriable

Summary:        Retriable is an simple DSL to retry failed code blocks with randomized exponential backoff.
Name:           rubygem-retriable
Version:        3.1.2
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=11061a8aa1413ae557ea6c7d0117a6554adf420f40c0c3a93f91bc86f97bf660ef9f3ebc5e56550351473fe8efa96169b27ececbc10b3381fee440fa08d8ef92

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Retriable is a simple DSL to retry failed code blocks with randomized exponential backoff.
This is especially useful when interacting external api/services or file system calls.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.2-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.2-1
- Initial version.
