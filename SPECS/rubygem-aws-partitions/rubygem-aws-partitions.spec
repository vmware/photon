%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-partitions

Name: rubygem-aws-partitions
Version:        1.96.0
Release:        1%{?dist}
Summary:        Provides interfaces to enumerate AWS partitions, regions & services.
Group:          Development/Languages
License:        Apache 2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-partitions-%{version}.gem
%define sha1    aws-partitions=162ffb14477764fd65153ba8c91c141b322ea87b
BuildRequires:  ruby

%description
Provides interfaces to enumerate AWS partitions, regions, and services.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.96.0-1
-   Initial build
