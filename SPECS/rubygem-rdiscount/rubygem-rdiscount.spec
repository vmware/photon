%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rdiscount

Name: rubygem-rdiscount
Version:        2.2.0.2
Release:        1%{?dist}
Summary:        Fast Implementation of Gruber's Markdown in C
Group:          Development/Languages
License:        BSD-3-CLAUSE
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    rdiscount=efbb7aee19ffff763a47a9c9b21d8ec901a3499e
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ruby > 1.9.2

%description
RDiscount converts documents in Markdown syntax to HTML.
It uses the excellent Discount processor by David Loren Parsons for this purpose,
and thereby inherits Discount’s numerous useful extensions to the Markdown language.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.2.0.2-1
-   Initial build
